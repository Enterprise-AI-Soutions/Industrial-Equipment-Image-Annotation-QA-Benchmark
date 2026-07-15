from src.calculate_iou import calculate_iou


def test_identical_boxes():
    box1 = [10, 10, 100, 100]
    box2 = [10, 10, 100, 100]

    assert calculate_iou(box1, box2) == 1.0


def test_non_overlapping_boxes():
    box1 = [0, 0, 50, 50]
    box2 = [100, 100, 50, 50]

    assert calculate_iou(box1, box2) == 0.0
