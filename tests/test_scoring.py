from src.schemas import Annotation
from src.schemas import BoundingBox

from src.quality_scoring import calculate_quality_score


def build_annotation():

    return Annotation(

        image_id="IMG001",

        annotation_id="ANN001",

        label="pump",

        confidence=0.90,

        bbox=BoundingBox(

            x=10,

            y=10,

            width=100,

            height=100,

        )

    )


def test_quality_score():

    prediction = build_annotation()

    ground_truth = build_annotation()

    result = calculate_quality_score(

        prediction,

        ground_truth,

    )

    assert result["status"] == "PASS"

    assert result["iou"] == 1.0

    assert result["quality_score"] > 0.9
