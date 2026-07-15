from src.schemas import Annotation


def test_annotation_creation():
    annotation = Annotation(
        image_id="IMG001",
        label="air_compressor",
        bbox=[20, 30, 200, 150],
        annotator="ANN001"
    )

    assert annotation.image_id == "IMG001"
    assert annotation.label == "air_compressor"
