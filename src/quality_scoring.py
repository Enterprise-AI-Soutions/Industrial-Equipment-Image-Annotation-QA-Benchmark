"""
Quality scoring for annotations.
"""

from src.calculate_iou import calculate_iou
from src.schemas import Annotation


def calculate_quality_score(
    prediction: Annotation,
    ground_truth: Annotation,
) -> dict:

    iou = calculate_iou(
        prediction.bbox,
        ground_truth.bbox,
    )

    label_score = (
        1
        if prediction.label == ground_truth.label
        else 0
    )

    confidence_score = prediction.confidence

    final_score = round(
        (
            iou * 0.6
            + label_score * 0.3
            + confidence_score * 0.1
        ),
        3,
    )

    status = "PASS" if final_score >= 0.80 else "FAIL"

    return {

        "image_id": prediction.image_id,

        "annotation_id": prediction.annotation_id,

        "iou": iou,

        "label_score": label_score,

        "confidence": confidence_score,

        "quality_score": final_score,

        "status": status

    }
