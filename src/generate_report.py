"""
Generate Markdown benchmark report.
"""

import json
from pathlib import Path
import pandas as pd


def generate_report():

    with open(
        "reports/validation_report.json",
        encoding="utf-8",
    ) as f:
        validation = json.load(f)

    with open(
        "reports/agreement_summary.json",
        encoding="utf-8",
    ) as f:
        agreement = json.load(f)

    review = pd.read_csv(
        "reports/review_queue.csv"
    )

    report = f"""# Industrial Equipment Image Annotation QA Benchmark

## Validation

Images Reviewed : {validation["images_reviewed"]}

Annotations : {validation["annotations"]}

Status : {validation["status"]}

---

## Reviewer Agreement

Agreement : {agreement["agreement"]:.2%}

Matching Labels : {agreement["matching_labels"]}

---

## Review Queue

Cases requiring review : {len(review)}

---

Generated automatically.
"""

    Path(
        "reports/annotation_report.md"
    ).write_text(
        report,
        encoding="utf-8",
    )

    print()

    print("Report generated successfully.")

    print("Output:")

    print("reports/annotation_report.md")


if __name__ == "__main__":

    generate_report()
