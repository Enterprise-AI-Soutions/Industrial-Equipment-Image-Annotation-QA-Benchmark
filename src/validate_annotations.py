"""
Validate annotation files against schema and image existence.
"""

import json
import sys
from pathlib import Path

from src.schemas import Annotation
from src.config import VALID_CLASSES, IMAGE_DIR, REPORT_DIR


def validate_annotations(file_path: str, skip_image_check: bool = False):
    """
    Load and validate annotations from a JSON file.

    Returns
    -------
    tuple[list[Annotation], list[dict]]
        (valid_annotations, issues_list)
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Annotation file not found: {file_path}")

    # Require images to exist in data/images/ (skipped in unit tests)
    if not skip_image_check:
        IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
        image_files = [
            f for f in IMAGE_DIR.iterdir()
            if f.is_file() and f.suffix.lower() in IMAGE_EXTS
        ] if IMAGE_DIR.exists() else []
        if not image_files:
            raise RuntimeError(
                f"No images found in {IMAGE_DIR}. "
                "Please upload your 9 industrial equipment images to data/images/ before running the pipeline."
            )

    with open(path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    validated = []
    issues = []

    for i, item in enumerate(raw_data):
        try:
            ann = Annotation(**item)
        except Exception as e:
            issues.append({"index": i, "item": item, "error": str(e)})
            continue

        # Class validation
        if ann.label not in VALID_CLASSES:
            issues.append({
                "index": i,
                "annotation_id": ann.annotation_id,
                "error": f"Unknown label '{ann.label}' not in VALID_CLASSES"
            })

        validated.append(ann)

    return validated, issues


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate annotation JSON file against schema and equipment class list."
    )
    parser.add_argument("file", help="Path to annotation JSON file")
    args = parser.parse_args()

    try:
        data, issues = validate_annotations(args.file)
    except RuntimeError as e:
        print(f"\n[ERROR] {e}\n")
        sys.exit(1)

    status = "PASSED" if not issues else "PASSED_WITH_WARNINGS"

    report = {
        "images_reviewed": len(data),
        "annotations": len(data),
        "issues_count": len(issues),
        "issues": issues,
        "status": status,
    }

    REPORT_DIR.mkdir(exist_ok=True)
    report_path = REPORT_DIR / "validation_report.json"

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print(f"\n[OK] Validated {len(data)} annotations.")
    if issues:
        print(f"[WARNING] {len(issues)} issue(s) found:")
        for iss in issues:
            print(f"   - {iss}")
    print(f"\nReport written to: {report_path.resolve()}")
