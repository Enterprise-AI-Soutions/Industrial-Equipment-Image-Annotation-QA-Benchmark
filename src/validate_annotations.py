"""
Validate annotation files against schema, class list, and actual image files.

For each annotation:
  1. Schema validation (Pydantic) - bbox format, required fields
  2. Class validation          - label is in VALID_CLASSES
  3. Image existence           - referenced image file found in data/images/
  4. BBox bounds check         - bbox fits within actual image dimensions
"""

import json
import sys
from pathlib import Path

from src.schemas import Annotation
from src.config import VALID_CLASSES, IMAGE_DIR, REPORT_DIR
from src.image_validator import ImageValidator, validate_annotation_with_image


def validate_annotations(file_path: str, skip_image_check: bool = False):
    """
    Load and validate annotations from a JSON file.

    Parameters
    ----------
    file_path : str
        Path to annotation JSON file.
    skip_image_check : bool
        If True, skip the image existence pre-flight and per-annotation image
        validation. Used in unit tests where no images are available.

    Returns
    -------
    tuple[list[Annotation], list[dict]]
        (valid_annotations, issues_list)
        issues_list contains schema errors, class warnings, and image violations.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Annotation file not found: {file_path}")

    # Pre-flight: require at least one image file in data/images/
    if not skip_image_check:
        IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
        image_files = [
            f for f in IMAGE_DIR.iterdir()
            if f.is_file() and f.suffix.lower() in IMAGE_EXTS
        ] if IMAGE_DIR.exists() else []
        if not image_files:
            raise RuntimeError(
                f"No images found in {IMAGE_DIR}. "
                "Please upload your 9 industrial equipment images to data/images/ "
                "before running the pipeline."
            )

    with open(path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    validator = ImageValidator(IMAGE_DIR) if not skip_image_check else None

    validated = []
    issues = []

    for i, item in enumerate(raw_data):
        ann_issues = []

        # --- 1. Schema validation ---
        try:
            ann = Annotation(**item)
        except Exception as e:
            issues.append({
                "index": i,
                "annotation_id": item.get("annotation_id", f"index_{i}"),
                "image_id": item.get("image_id", ""),
                "stage": "schema",
                "error": str(e),
            })
            continue

        # --- 2. Class validation ---
        if ann.label not in VALID_CLASSES:
            ann_issues.append(f"Unknown label '{ann.label}' not in VALID_CLASSES")

        # --- 3 & 4. Image existence + BBox bounds (uses real image files) ---
        image_info = {}
        if validator is not None:
            image_ref = item.get("image", "")
            bbox_raw = item.get("bbox", [])

            is_valid, img_errors, image_info = validate_annotation_with_image(
                {"image": image_ref, "bbox": bbox_raw},
                validator,
            )
            validator.clear_errors()

            if img_errors:
                ann_issues.extend(img_errors)

        if ann_issues:
            issues.append({
                "index": i,
                "annotation_id": ann.annotation_id,
                "image_id": ann.image_id,
                "image_ref": item.get("image", ""),
                "resolved_image": image_info.get("resolved_filename"),
                "image_width": image_info.get("image_width"),
                "image_height": image_info.get("image_height"),
                "stage": "image_validation",
                "errors": ann_issues,
            })

        # Store image info on the annotation object for downstream use
        ann.image_filename = image_info.get("resolved_filename") or item.get("image")
        validated.append(ann)

    return validated, issues


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Validate annotation JSON file against schema, class list, "
            "and actual image files in data/images/."
        )
    )
    parser.add_argument("file", help="Path to annotation JSON file")
    args = parser.parse_args()

    try:
        data, issues = validate_annotations(args.file)
    except RuntimeError as e:
        print(f"\n[ERROR] {e}\n")
        sys.exit(1)

    # ---- Summary ----
    schema_errors = [i for i in issues if i.get("stage") == "schema"]
    image_issues  = [i for i in issues if i.get("stage") == "image_validation"]

    status = "PASSED" if not schema_errors else "FAILED"
    if image_issues and not schema_errors:
        status = "PASSED_WITH_IMAGE_WARNINGS"

    # ---- Per-annotation image info for report ----
    image_validation_details = []
    for iss in image_issues:
        image_validation_details.append({
            "annotation_id":    iss.get("annotation_id"),
            "image_id":         iss.get("image_id"),
            "image_ref":        iss.get("image_ref"),
            "resolved_image":   iss.get("resolved_image"),
            "image_width":      iss.get("image_width"),
            "image_height":     iss.get("image_height"),
            "errors":           iss.get("errors", []),
        })

    report = {
        "images_reviewed":          len(data),
        "annotations":              len(data),
        "schema_errors":            len(schema_errors),
        "image_validation_issues":  len(image_issues),
        "issues_count":             len(issues),
        "status":                   status,
        "image_validation_details": image_validation_details,
        "schema_issues":            schema_errors,
    }

    REPORT_DIR.mkdir(exist_ok=True)
    report_path = REPORT_DIR / "validation_report.json"

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    # ---- Console output ----
    print(f"\n[OK] Validated {len(data)} annotations.")

    if schema_errors:
        print(f"[ERROR] {len(schema_errors)} schema error(s):")
        for se in schema_errors:
            print(f"   [{se['annotation_id']}] {se['error']}")

    if image_issues:
        print(f"\n[WARNING] {len(image_issues)} annotation(s) with image validation issues:")
        for iss in image_issues:
            print(f"\n   Annotation : {iss['annotation_id']}  (Image ID: {iss['image_id']})")
            print(f"   Referenced : {iss['image_ref']}")
            print(f"   Resolved   : {iss.get('resolved_image', 'NOT FOUND')}")
            if iss.get("image_width"):
                print(f"   Dimensions : {iss['image_width']} x {iss['image_height']} px")
            for err in iss.get("errors", []):
                print(f"   Issue      : {err}")
    else:
        print("[OK] All annotations passed image validation (files found, bbox within bounds).")

    print(f"\nReport written to: {report_path.resolve()}")
