"""
Tests for IoU-based duplicate bounding box detection.
"""

from src.schemas import Annotation, BoundingBox
from src.duplicate_detection import find_duplicate_boxes


def make_annotation(image_id, annotation_id, x, y, w, h, label="pump"):
    return Annotation(
        image_id=image_id,
        annotation_id=annotation_id,
        label=label,
        confidence=0.90,
        bbox=BoundingBox(x=x, y=y, width=w, height=h),
    )


def test_no_duplicates():
    """Two non-overlapping boxes in the same image should produce no duplicates."""
    anns = [
        make_annotation("IMG001", "ANN001", 0, 0, 50, 50),
        make_annotation("IMG001", "ANN002", 300, 300, 50, 50),
    ]
    dups = find_duplicate_boxes(anns, iou_threshold=0.5)
    assert dups == []


def test_exact_duplicate():
    """Two identical boxes in same image should be flagged as duplicates."""
    anns = [
        make_annotation("IMG001", "ANN001", 10, 10, 100, 100),
        make_annotation("IMG001", "ANN002", 10, 10, 100, 100),
    ]
    dups = find_duplicate_boxes(anns, iou_threshold=0.5)
    assert len(dups) == 1
    assert dups[0]["iou"] == 1.0


def test_different_images_not_flagged():
    """Identical boxes in different images should NOT be flagged."""
    anns = [
        make_annotation("IMG001", "ANN001", 10, 10, 100, 100),
        make_annotation("IMG002", "ANN002", 10, 10, 100, 100),
    ]
    dups = find_duplicate_boxes(anns, iou_threshold=0.5)
    assert dups == []


def test_high_overlap_flagged():
    """Boxes with IoU above threshold should be flagged."""
    # Box1=(0,0,100,100), Box2=(10,10,100,100)
    # Intersection = 90*90 = 8100, Union = 10000+10000-8100 = 11900
    # IoU = 8100/11900 ≈ 0.681 > 0.5 threshold
    anns = [
        make_annotation("IMG001", "ANN001", 0, 0, 100, 100),
        make_annotation("IMG001", "ANN002", 10, 10, 100, 100),
    ]
    dups = find_duplicate_boxes(anns, iou_threshold=0.5)
    assert len(dups) == 1
    assert dups[0]["iou"] > 0.5
