from src.schemas import BoundingBox
from src.calculate_iou import calculate_iou


def test_identical_boxes():

    box1 = BoundingBox(
        x=10,
        y=10,
        width=100,
        height=100,
    )

    box2 = BoundingBox(
        x=10,
        y=10,
        width=100,
        height=100,
    )

    assert calculate_iou(box1, box2) == 1.0


def test_partial_overlap():

    box1 = BoundingBox(
        x=0,
        y=0,
        width=100,
        height=100,
    )

    box2 = BoundingBox(
        x=50,
        y=50,
        width=100,
        height=100,
    )

    iou = calculate_iou(box1, box2)

    assert 0 < iou < 1


def test_no_overlap():

    box1 = BoundingBox(
        x=0,
        y=0,
        width=100,
        height=100,
    )

    box2 = BoundingBox(
        x=300,
        y=300,
        width=50,
        height=50,
    )

    assert calculate_iou(box1, box2) == 0.0
