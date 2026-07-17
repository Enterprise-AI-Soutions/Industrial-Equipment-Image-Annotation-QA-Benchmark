"""
Create manual review queue.
Flags annotations requiring human review based on:
  - Label disagreement between annotators
  - Low IoU (< IOU_THRESHOLD)
  - Low confidence score (< REVIEW_QUEUE_THRESHOLD)
"""

import csv
import json
from pathlib import Path

from src.schemas import Annotation
from src.calculate_iou import calculate_iou
from src.config import IOU_THRESHOLD, REVIEW_QUEUE_THRESHOLD, REPORT_DIR


def create_review_queue(file1: str, file2: str, output: str) -> int:
    """
    Generate a review queue CSV from two annotator files.

    Parameters
    ----------
    file1, file2 : str
        Paths to annotator JSON files.
    output : str
        Path for the output CSV file.

    Returns
    -------
    int
        Number of review cases created.
    """
    with open(file1, encoding="utf-8") as f:
        raw1 = json.load(f)
    with open(file2, encoding="utf-8") as f:
        raw2 = json.load(f)

    # Parse through Pydantic (normalises labels, handles array bbox + extra fields)
    ann1 = [Annotation(**item) for item in raw1]
    ann2 = [Annotation(**item) for item in raw2]

    rows = []

    for a1, a2 in zip(ann1, ann2):
        reasons = []

        # 1. Label disagreement
        if a1.label != a2.label:
            reasons.append("Label disagreement")

        # 2. Low IoU (spatial disagreement)
        iou = calculate_iou(a1.bbox, a2.bbox)
        if iou < IOU_THRESHOLD:
            reasons.append(f"Low IoU ({iou:.3f} < {IOU_THRESHOLD})")

        # 3. Low confidence (either annotator)
        if a1.confidence < REVIEW_QUEUE_THRESHOLD:
            reasons.append(f"Low confidence annotator_1 ({a1.confidence:.2f})")
        if a2.confidence < REVIEW_QUEUE_THRESHOLD:
            reasons.append(f"Low confidence annotator_2 ({a2.confidence:.2f})")

        if reasons:
            rows.append({
                "image_id": a1.image_id,
                "annotation_id": a1.annotation_id,
                "annotator_1_label": a1.label,
                "annotator_2_label": a2.label,
                "iou": round(iou, 3),
                "annotator_1_confidence": a1.confidence,
                "annotator_2_confidence": a2.confidence,
                "review_reason": " | ".join(reasons),
            })

    Path(output).parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "image_id",
        "annotation_id",
        "annotator_1_label",
        "annotator_2_label",
        "iou",
        "annotator_1_confidence",
        "annotator_2_confidence",
        "review_reason",
    ]

    with open(output, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Create a review queue CSV from two annotator files."
    )
    parser.add_argument("evaluator1", help="Path to annotator 1 JSON file")
    parser.add_argument("evaluator2", help="Path to annotator 2 JSON file")
    parser.add_argument("output", help="Output CSV path")
    args = parser.parse_args()

    total = create_review_queue(args.evaluator1, args.evaluator2, args.output)

    print(f"\n✔ Review queue written to: {args.output}")
    print(f"  {total} annotation(s) flagged for review.")
