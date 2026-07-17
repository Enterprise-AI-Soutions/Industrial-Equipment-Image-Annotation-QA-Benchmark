"""
Reviewer agreement analysis — label agreement and IoU-based spatial agreement.
"""

import json
from pathlib import Path

from src.schemas import Annotation
from src.calculate_iou import calculate_iou
from src.config import REPORT_DIR


def calculate_agreement(file1: str, file2: str) -> dict:
    """
    Compute inter-annotator agreement between two annotation files.

    Calculates:
    - Label agreement rate (exact match after normalisation)
    - Mean IoU across matched pairs
    - Per-label breakdown

    Parameters
    ----------
    file1, file2 : str
        Paths to annotator JSON files.

    Returns
    -------
    dict
        Agreement summary with label and IoU scores.
    """
    with open(file1, "r", encoding="utf-8") as f:
        raw1 = json.load(f)
    with open(file2, "r", encoding="utf-8") as f:
        raw2 = json.load(f)

    # Parse and normalise using Pydantic (handles bbox array format, extra fields, lowercase labels)
    ann1 = [Annotation(**item) for item in raw1]
    ann2 = [Annotation(**item) for item in raw2]

    total = min(len(ann1), len(ann2))
    label_matches = 0
    iou_scores = []
    per_label: dict[str, dict] = {}

    for a1, a2 in zip(ann1, ann2):
        # Label agreement (already lowercased by schema)
        label_match = int(a1.label == a2.label)
        label_matches += label_match

        # Spatial agreement via IoU
        iou = calculate_iou(a1.bbox, a2.bbox)
        iou_scores.append(iou)

        # Per-label breakdown keyed by annotator-1 label
        entry = per_label.setdefault(a1.label, {"total": 0, "label_matches": 0, "iou_sum": 0.0})
        entry["total"] += 1
        entry["label_matches"] += label_match
        entry["iou_sum"] += iou

    mean_iou = round(sum(iou_scores) / len(iou_scores), 3) if iou_scores else 0.0
    label_agreement = round(label_matches / total, 3) if total else 0.0

    # Build per-label summary
    per_label_summary = {
        label: {
            "count": v["total"],
            "label_agreement": round(v["label_matches"] / v["total"], 3),
            "mean_iou": round(v["iou_sum"] / v["total"], 3),
        }
        for label, v in per_label.items()
    }

    return {
        "total_annotations": total,
        "matching_labels": label_matches,
        "agreement": label_agreement,
        "mean_iou": mean_iou,
        "per_label": per_label_summary,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate inter-annotator agreement between two annotation files."
    )
    parser.add_argument("evaluator1", help="Path to annotator 1 JSON file")
    parser.add_argument("evaluator2", help="Path to annotator 2 JSON file")
    args = parser.parse_args()

    result = calculate_agreement(args.evaluator1, args.evaluator2)

    REPORT_DIR.mkdir(exist_ok=True)
    output = REPORT_DIR / "agreement_summary.json"

    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print(f"\n✔ Agreement summary written to: {output}")
    print(f"  Label agreement : {result['agreement']:.1%}")
    print(f"  Mean IoU        : {result['mean_iou']:.3f}")
    print(f"  Matching labels : {result['matching_labels']} / {result['total_annotations']}")
