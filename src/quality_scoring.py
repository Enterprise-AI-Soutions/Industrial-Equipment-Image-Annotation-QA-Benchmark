"""
Quality scoring for annotations.
Scores each annotation against ground truth using IoU, label match, and confidence.
"""

from src.calculate_iou import calculate_iou
from src.schemas import Annotation
from src.config import QUALITY_PASS_SCORE


def calculate_quality_score(
    prediction: Annotation,
    ground_truth: Annotation,
) -> dict:
    """
    Score a single annotation against its ground truth.

    Scoring weights:
    - IoU          : 60%
    - Label match  : 30%
    - Confidence   : 10%

    Returns
    -------
    dict
        {image_id, annotation_id, iou, label_score, confidence, quality_score, status}
    """
    iou = calculate_iou(prediction.bbox, ground_truth.bbox)

    label_score = 1 if prediction.label == ground_truth.label else 0

    confidence_score = prediction.confidence

    final_score = round(
        iou * 0.6 + label_score * 0.3 + confidence_score * 0.1,
        3,
    )

    # Use threshold from config instead of hardcoded 0.80
    status = "PASS" if final_score >= QUALITY_PASS_SCORE else "FAIL"

    return {
        "image_id": prediction.image_id,
        "annotation_id": prediction.annotation_id,
        "iou": iou,
        "label_score": label_score,
        "confidence": confidence_score,
        "quality_score": final_score,
        "status": status,
    }


def score_all_annotations(
    predictions: list[Annotation],
    ground_truths: list[Annotation],
) -> list[dict]:
    """
    Batch-score a list of annotations against ground truths.
    Matches by annotation_id.

    Returns
    -------
    list[dict]
        List of quality score results for each matched pair.
    """
    gt_by_id = {ann.annotation_id: ann for ann in ground_truths}
    results = []

    for pred in predictions:
        gt = gt_by_id.get(pred.annotation_id)
        if gt is None:
            results.append({
                "image_id": pred.image_id,
                "annotation_id": pred.annotation_id,
                "iou": None,
                "label_score": None,
                "confidence": pred.confidence,
                "quality_score": None,
                "status": "NO_GROUND_TRUTH",
            })
        else:
            results.append(calculate_quality_score(pred, gt))

    return results
