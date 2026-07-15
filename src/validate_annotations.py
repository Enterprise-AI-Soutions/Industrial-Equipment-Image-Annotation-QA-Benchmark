"""
Validate annotation files.
"""

import json
from pathlib import Path

from src.schemas import Annotation


def validate_annotations(file_path: str):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(file_path)

    with open(path, "r", encoding="utf-8") as f:

        annotations = json.load(f)

    validated = []

    for item in annotations:

        validated.append(

            Annotation(**item)

        )

    return validated


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("file")

    args = parser.parse_args()

    data = validate_annotations(args.file)

    report = {
    "images_reviewed": len(validated),
    "annotations": len(validated),
    "status": "PASSED"
}

with open(
    "reports/validation_report.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(report, f, indent=4)

print(f"Validated {len(validated)} annotations.")

print("Validation report saved to reports/validation_report.json")
