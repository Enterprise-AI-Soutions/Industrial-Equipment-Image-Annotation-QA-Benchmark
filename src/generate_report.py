"""
Generate Markdown benchmark report and annotation_summary.csv.
Reads all intermediate report files and produces a consolidated report
including per-image validation results using actual image dimensions.
"""

import json
import csv
from datetime import datetime
from pathlib import Path

import pandas as pd
from PIL import Image

from src.config import REPORT_DIR, ANNOTATION_DIR, IMAGE_DIR
from src.image_validator import resolve_image_file


# ---------------------------------------------------------------------------
# Safe loaders
# ---------------------------------------------------------------------------

def _load_json_safe(path: Path, default=None):
    """Load JSON file, returning default if missing or invalid."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _load_csv_safe(path: Path):
    """Load CSV, returning empty DataFrame if missing."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# Per-image summary builder (uses actual image files)
# ---------------------------------------------------------------------------

def _get_real_image_dimensions(image_ref: str) -> tuple:
    """Load actual image from data/images/ and return (width, height)."""
    resolved = resolve_image_file(image_ref, IMAGE_DIR)
    if resolved is None:
        return None, None
    try:
        with Image.open(resolved) as img:
            return img.size  # (width, height)
    except Exception:
        return None, None


def generate_annotation_summary() -> pd.DataFrame:
    """
    Build per-image annotation summary from both annotator files.
    Loads ACTUAL image dimensions from data/images/ using Pillow.
    Writes annotation_summary.csv.
    """
    ann1_path = ANNOTATION_DIR / "annotator_1.json"
    ann2_path = ANNOTATION_DIR / "annotator_2.json"

    try:
        with open(ann1_path, encoding="utf-8") as f:
            ann1 = json.load(f)
        with open(ann2_path, encoding="utf-8") as f:
            ann2 = json.load(f)
    except FileNotFoundError:
        return pd.DataFrame()

    ann2_by_id = {a["annotation_id"]: a for a in ann2}

    rows = []
    for a in ann1:
        a2 = ann2_by_id.get(a.get("annotation_id", ""), {})
        image_ref = a.get("image", "")

        # Load real image dimensions
        resolved = resolve_image_file(image_ref, IMAGE_DIR)
        resolved_name = resolved.name if resolved else "NOT FOUND"
        img_w, img_h = _get_real_image_dimensions(image_ref)

        # BBox info
        bbox = a.get("bbox", [0, 0, 0, 0])
        bbox_str = f"[{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}]" if len(bbox) == 4 else ""

        # Check bbox within bounds
        bbox_ok = "N/A"
        if img_w and len(bbox) == 4:
            x, y, w, h = bbox
            bbox_ok = "OK" if (x >= 0 and y >= 0 and x + w <= img_w and y + h <= img_h) else "OUT_OF_BOUNDS"

        rows.append({
            "image_id":              a.get("image_id", ""),
            "annotation_id":         a.get("annotation_id", ""),
            "referenced_filename":   image_ref,
            "resolved_filename":     resolved_name,
            "real_width_px":         img_w if img_w else "N/A",
            "real_height_px":        img_h if img_h else "N/A",
            "annotator_1_label":     str(a.get("label", "")).lower().strip(),
            "annotator_2_label":     str(a2.get("label", "")).lower().strip() if a2 else "",
            "annotator_1_conf":      a.get("confidence", ""),
            "annotator_2_conf":      a2.get("confidence", "") if a2 else "",
            "bbox":                  bbox_str,
            "bbox_within_bounds":    bbox_ok,
        })

    df = pd.DataFrame(rows)
    REPORT_DIR.mkdir(exist_ok=True)
    df.to_csv(REPORT_DIR / "annotation_summary.csv", index=False)
    return df


# ---------------------------------------------------------------------------
# Main report generator
# ---------------------------------------------------------------------------

def generate_report():
    """Generate the consolidated Markdown QA benchmark report."""

    # Load intermediate reports
    validation  = _load_json_safe(REPORT_DIR / "validation_report.json", default={})
    agreement   = _load_json_safe(REPORT_DIR / "agreement_summary.json", default={})
    review      = _load_csv_safe(REPORT_DIR / "review_queue.csv")
    duplicates  = _load_csv_safe(REPORT_DIR / "duplicate_boxes.csv")

    # Build annotation summary (reads real images)
    summary_df = generate_annotation_summary()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Validation section ---
    val_images      = validation.get("images_reviewed", "N/A")
    val_annotations = validation.get("annotations", "N/A")
    val_status      = validation.get("status", "N/A")
    val_schema_err  = validation.get("schema_errors", 0)
    val_img_issues  = validation.get("image_validation_issues", 0)

    # --- Agreement section ---
    agr_score   = agreement.get("agreement", 0)
    agr_iou     = agreement.get("mean_iou", 0)
    agr_matches = agreement.get("matching_labels", "N/A")
    agr_total   = agreement.get("total_annotations", "N/A")

    # --- Per-label agreement table ---
    per_label = agreement.get("per_label", {})
    per_label_rows = ""
    for label, stats in per_label.items():
        per_label_rows += (
            f"| {label:<22} | {stats['count']:>5} | "
            f"{stats['label_agreement']:>16.1%} | "
            f"{stats['mean_iou']:>8.3f} |\n"
        )

    # --- Per-image validation table (from summary CSV) ---
    img_table_rows = ""
    if not summary_df.empty:
        for _, row in summary_df.iterrows():
            status_cell = "[OK]" if row["bbox_within_bounds"] == "OK" else str(row["bbox_within_bounds"])
            img_table_rows += (
                f"| {row['image_id']:<8} | {str(row['resolved_filename']):<28} | "
                f"{str(row['real_width_px']):>7} | {str(row['real_height_px']):>7} | "
                f"{str(row['annotator_1_label']):<20} | {str(row['bbox']):<22} | "
                f"{status_cell:<15} |\n"
            )

    # --- Image validation details from validation report ---
    img_val_detail_section = ""
    img_details = validation.get("image_validation_details", [])
    if img_details:
        img_val_detail_section = "\n### Image Validation Issues\n\n"
        for d in img_details:
            img_val_detail_section += (
                f"- **{d['annotation_id']}** (`{d['image_ref']}` -> "
                f"`{d.get('resolved_image', 'NOT FOUND')}`)"
                f" {d['image_width']}x{d['image_height']}px: "
                + "; ".join(d.get("errors", [])) + "\n"
            )
    else:
        img_val_detail_section = "\nAll images resolved and bounding boxes validated successfully.\n"

    # --- Review queue ---
    review_count   = len(review)
    review_reasons = ""
    if review_count > 0 and "review_reason" in review.columns:
        for reason, cnt in review["review_reason"].value_counts().items():
            review_reasons += f"  - {reason}: {cnt}\n"

    dup_count = len(duplicates)

    report = f"""# Industrial Equipment Image Annotation QA Benchmark

Generated: {timestamp}

---

## Validation Results

| Metric                      | Value         |
|-----------------------------|---------------|
| Images Reviewed             | {val_images}  |
| Annotations Validated       | {val_annotations} |
| Schema Errors               | {val_schema_err}  |
| Image Validation Issues     | {val_img_issues}  |
| Overall Status              | {val_status}  |

---

## Per-Image Validation (Actual Image Files)

| Image ID | Resolved Filename             | Width   | Height  | Label                | BBox                   | BBox Status     |
|----------|-------------------------------|---------|---------|----------------------|------------------------|-----------------|
{img_table_rows}
{img_val_detail_section}

---

## Reviewer Agreement

| Metric              | Value         |
|---------------------|---------------|
| Label Agreement     | {agr_score:.1%} |
| Mean IoU            | {agr_iou:.3f} |
| Matching Labels     | {agr_matches} / {agr_total} |

### Per-Label Breakdown

| Label                  | Count | Label Agreement  | Mean IoU |
|------------------------|-------|------------------|----------|
{per_label_rows}
---

## Duplicate Detection

Near-duplicate bounding boxes detected (IoU >= threshold): **{dup_count}**

---

## Review Queue

Annotations flagged for manual review: **{review_count}**

{review_reasons}
---

## Output Files

| File                            | Description                             |
|---------------------------------|-----------------------------------------|
| reports/validation_report.json  | Schema + image + class validation       |
| reports/agreement_summary.json  | Inter-annotator label + IoU agreement   |
| reports/review_queue.csv        | Annotations flagged for review          |
| reports/duplicate_boxes.csv     | Near-duplicate bounding boxes           |
| reports/annotation_summary.csv  | Per-image: real dims, bbox status       |

---

*Generated automatically by Industrial Equipment Image Annotation QA Benchmark.*
"""

    out_path = REPORT_DIR / "annotation_report.md"
    out_path.write_text(report, encoding="utf-8")

    print("\n[OK] Report generated successfully.")
    print(f"  Output           : {out_path.resolve()}")
    print(f"  Annotation summary : {(REPORT_DIR / 'annotation_summary.csv').resolve()}")


if __name__ == "__main__":
    generate_report()
