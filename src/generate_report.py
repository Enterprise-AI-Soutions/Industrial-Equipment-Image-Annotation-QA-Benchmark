"""
Generate Markdown benchmark report and annotation_summary.csv.
Reads all intermediate report files and produces a consolidated report.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.config import REPORT_DIR, ANNOTATION_DIR


def _load_json_safe(path: Path, default=None):
    """Load JSON file, returning default if file is missing or invalid."""
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


def generate_annotation_summary() -> pd.DataFrame:
    """
    Build per-image annotation summary from annotator 1 file.
    Returns DataFrame and writes annotation_summary.csv.
    """
    import json

    ann1_path = ANNOTATION_DIR / "annotator_1.json"
    ann2_path = ANNOTATION_DIR / "annotator_2.json"

    try:
        with open(ann1_path) as f:
            ann1 = json.load(f)
        with open(ann2_path) as f:
            ann2 = json.load(f)
    except FileNotFoundError:
        return pd.DataFrame()

    rows = []
    ann2_by_id = {a["annotation_id"]: a for a in ann2}

    for a in ann1:
        a2 = ann2_by_id.get(a.get("annotation_id", ""), {})
        rows.append({
            "image_id": a.get("image_id", ""),
            "annotation_id": a.get("annotation_id", ""),
            "annotator_1_label": str(a.get("label", "")).lower().strip(),
            "annotator_2_label": str(a2.get("label", "")).lower().strip() if a2 else "",
            "annotator_1_confidence": a.get("confidence", ""),
            "annotator_2_confidence": a2.get("confidence", "") if a2 else "",
        })

    df = pd.DataFrame(rows)
    out_path = REPORT_DIR / "annotation_summary.csv"
    REPORT_DIR.mkdir(exist_ok=True)
    df.to_csv(out_path, index=False)
    return df


def generate_report():
    """Generate the consolidated Markdown QA benchmark report."""

    # Load intermediate reports
    validation = _load_json_safe(REPORT_DIR / "validation_report.json", default={})
    agreement = _load_json_safe(REPORT_DIR / "agreement_summary.json", default={})
    review = _load_csv_safe(REPORT_DIR / "review_queue.csv")
    duplicates = _load_csv_safe(REPORT_DIR / "duplicate_boxes.csv")

    # Generate annotation summary CSV
    summary_df = generate_annotation_summary()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Validation section ---
    val_images = validation.get("images_reviewed", "N/A")
    val_annotations = validation.get("annotations", "N/A")
    val_status = validation.get("status", "N/A")
    val_issues = validation.get("issues_count", 0)

    # --- Agreement section ---
    agr_score = agreement.get("agreement", 0)
    agr_iou = agreement.get("mean_iou", 0)
    agr_matches = agreement.get("matching_labels", "N/A")
    agr_total = agreement.get("total_annotations", "N/A")

    # --- Per-label agreement ---
    per_label = agreement.get("per_label", {})
    per_label_rows = ""
    for label, stats in per_label.items():
        per_label_rows += (
            f"| {label:<20} | {stats['count']:>5} | "
            f"{stats['label_agreement']:>16.1%} | "
            f"{stats['mean_iou']:>8.3f} |\n"
        )

    # --- Review queue section ---
    review_count = len(review)
    review_reasons = ""
    if review_count > 0 and "review_reason" in review.columns:
        reason_counts = review["review_reason"].value_counts()
        for reason, cnt in reason_counts.items():
            review_reasons += f"  - {reason}: {cnt}\n"

    # --- Duplicate section ---
    dup_count = len(duplicates)

    report = f"""# Industrial Equipment Image Annotation QA Benchmark

Generated: {timestamp}

---

## Validation Results

| Metric              | Value         |
|---------------------|---------------|
| Images Reviewed     | {val_images}  |
| Annotations Parsed  | {val_annotations} |
| Issues Found        | {val_issues}  |
| Status              | {val_status}  |

---

## Reviewer Agreement

| Metric              | Value         |
|---------------------|---------------|
| Label Agreement     | {agr_score:.1%} |
| Mean IoU            | {agr_iou:.3f} |
| Matching Labels     | {agr_matches} / {agr_total} |

### Per-Label Breakdown

| Label                | Count | Label Agreement  | Mean IoU |
|----------------------|-------|------------------|----------|
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

| File                            | Description                        |
|---------------------------------|------------------------------------|
| reports/validation_report.json  | Schema + class validation results  |
| reports/agreement_summary.json  | Inter-annotator agreement scores   |
| reports/review_queue.csv        | Annotations flagged for review     |
| reports/duplicate_boxes.csv     | Near-duplicate bounding boxes      |
| reports/annotation_summary.csv  | Per-image annotation overview      |

---

*Generated automatically by Industrial Equipment Image Annotation QA Benchmark.*
"""

    out_path = REPORT_DIR / "annotation_report.md"
    out_path.write_text(report, encoding="utf-8")

    print("\n[OK] Report generated successfully.")
    print(f"  Output: {out_path.resolve()}")
    print(f"  Annotation summary: {(REPORT_DIR / 'annotation_summary.csv').resolve()}")


if __name__ == "__main__":
    generate_report()
