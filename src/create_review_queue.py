"""
Create manual review queue.
"""

import csv
import json


def create_review_queue(file1, file2, output):

    with open(file1) as f:
        ann1 = json.load(f)

    with open(file2) as f:
        ann2 = json.load(f)

    rows = []

    for a1, a2 in zip(ann1, ann2):

        if a1["label"] != a2["label"]:

            rows.append({

                "image_id": a1["image_id"],

                "annotation_id": a1["annotation_id"],

                "review_reason": "Label disagreement",

            })

    with open(output, "w", newline="") as csvfile:

        writer = csv.DictWriter(

            csvfile,

            fieldnames=[
                "image_id",
                "annotation_id",
                "review_reason",
            ],
        )

        writer.writeheader()

        writer.writerows(rows)

    return len(rows)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("evaluator1")

    parser.add_argument("evaluator2")

    parser.add_argument("output")

    args = parser.parse_args()

    total = create_review_queue(
        args.evaluator1,
        args.evaluator2,
        args.output,
    )

    print(f"{total} review cases created.")
