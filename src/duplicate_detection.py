"""
Duplicate annotation detection using IoU-based comparison.
Detects near-duplicate bounding boxes within the same image.
"""

import csv
from pathlib import Path

from src.calculate_iou import calculate_iou
from src.schemas import BoundingBox
from src.config import IOU_THRESHOLD, REPORT_DIR


def find_duplicates(items):
    """Find duplicate string items (legacy helper)."""
    from collections import Counter
    counts = Counter(items)
    return [k for k, v in counts.items() if v > 1]


def find_duplicate_boxes(annotations: list, iou_threshold: float = IOU_THRESHOLD) -> list[dict]:
    """
    Detect near-duplicate bounding boxes within the same image using IoU.

    Parameters
    ----------
    annotations : list[Annotation]
        List of validated Annotation objects.
    iou_threshold : float
        IoU value above which two boxes are considered duplicates.

    Returns
    -------
    list[dict]
        Each dict describes a duplicate pair:
        {image_id, annotation_id_1, annotation_id_2, label_1, label_2, iou}
    """
    # Group by image_id
    by_image: dict[str, list] = {}
    for ann in annotations:
        by_image.setdefault(ann.image_id, []).append(ann)

    duplicates = []

    for image_id, anns in by_image.items():
        for i in range(len(anns)):
            for j in range(i + 1, len(anns)):
                a1, a2 = anns[i], anns[j]
                iou = calculate_iou(a1.bbox, a2.bbox)
                if iou >= iou_threshold:
                    duplicates.append({
                        "image_id": image_id,
                        "annotation_id_1": a1.annotation_id,
                        "annotation_id_2": a2.annotation_id,
                        "label_1": a1.label,
                        "label_2": a2.label,
                        "iou": round(iou, 3),
                    })

    return duplicates


def write_duplicate_report(duplicates: list[dict], output_path: Path | None = None) -> Path:
    """Write duplicate detection results to CSV."""
    if output_path is None:
        output_path = REPORT_DIR / "duplicate_boxes.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["image_id", "annotation_id_1", "annotation_id_2", "label_1", "label_2", "iou"]

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(duplicates)

    return output_path
