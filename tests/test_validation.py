import json

from src.validate_annotations import validate_annotations


def test_validate_annotations(tmp_path):

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

                "height": 80

            }

        }

    ]

    test_file = tmp_path / "annotations.json"

    with open(test_file, "w", encoding="utf-8") as f:

        json.dump(sample, f)

    validated = validate_annotations(test_file)

    assert len(validated) == 1

    assert validated[0].label == "pump"
