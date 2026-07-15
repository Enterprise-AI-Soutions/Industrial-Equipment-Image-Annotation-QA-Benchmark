"""
Reviewer agreement analysis.
"""

import json


def calculate_agreement(file1, file2):

    with open(file1, "r", encoding="utf-8") as f:
        ann1 = json.load(f)

    with open(file2, "r", encoding="utf-8") as f:
        ann2 = json.load(f)

    total = min(len(ann1), len(ann2))

    matches = 0

    for a1, a2 in zip(ann1, ann2):

        if a1["label"] == a2["label"]:

            matches += 1

    agreement = round(matches / total, 3)

    return {

        "total_annotations": total,

        "matching_labels": matches,

        "agreement": agreement,

    }


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("evaluator1")

    parser.add_argument("evaluator2")

    args = parser.parse_args()

    result = calculate_agreement(
        args.evaluator1,
        args.evaluator2,
    )

    with open(
    "reports/agreement_summary.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(result, f, indent=4)

from pathlib import Path

Path("reports").mkdir(exist_ok=True)

with open(
    "reports/agreement_summary.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(result, f, indent=4)

print(result)

print("Agreement summary saved to reports/agreement_summary.json")
