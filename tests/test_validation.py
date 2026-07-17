"""
Tests for annotation validation — schema parsing and class checks.
"""

import json

from src.validate_annotations import validate_annotations


def test_validate_annotations_dict_bbox(tmp_path):
    """Annotations with dict-format bbox should validate successfully."""
    sample = [
        {
            "image_id": "IMG001",
            "annotation_id": "ANN001",
            "label": "pump",
            "confidence": 0.95,
            "bbox": {
                "x": 10,
                "y": 20,
                "width": 100,
                "height": 80,
            },
        }
    ]

    test_file = tmp_path / "annotations.json"
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(sample, f)

    validated, issues = validate_annotations(test_file, skip_image_check=True)

    assert len(validated) == 1
    assert validated[0].label == "pump"
    assert issues == []


def test_validate_annotations_array_bbox(tmp_path):
    """Annotations with array-format bbox [x, y, w, h] should parse correctly."""
    sample = [
        {
            "id": 1,
            "image_id": "IMG002",
            "annotation_id": "ANN002",
            "image": "valve.jpg",
            "label": "valve",
            "confidence": 0.88,
            "bbox": [120, 85, 220, 165],   # array format
        }
    ]

    test_file = tmp_path / "annotations_array.json"
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(sample, f)

    validated, issues = validate_annotations(test_file, skip_image_check=True)

    assert len(validated) == 1
    assert validated[0].label == "valve"
    assert validated[0].bbox.x == 120
    assert validated[0].bbox.width == 220


def test_label_normalised_to_lowercase(tmp_path):
    """Labels should be normalised to lowercase regardless of input casing."""
    sample = [
        {
            "image_id": "IMG003",
            "annotation_id": "ANN003",
            "label": "PUMP",
            "confidence": 0.90,
            "bbox": {"x": 0, "y": 0, "width": 100, "height": 100},
        }
    ]

    test_file = tmp_path / "annotations_upper.json"
    with open(test_file, "w", encoding="utf-8") as f:
        json.dump(sample, f)

    validated, _ = validate_annotations(test_file, skip_image_check=True)

    assert validated[0].label == "pump"
