"""
Generate Markdown benchmark report.
"""

from pathlib import Path
import pandas as pd


def generate_report(
    scoring_csv,
    agreement,
    review_queue,
    output,
):

    score_df = pd.read_csv(scoring_csv)

    review_df = pd.read_csv(review_queue)

    report = f"""
# Industrial Equipment Image Annotation QA Benchmark

## Summary

Total annotations : {len(score_df)}

Average IoU : {score_df['iou'].mean():.3f}

Average Quality Score : {score_df['quality_score'].mean():.3f}

Passed : {(score_df['status']=='PASS').sum()}

Failed : {(score_df['status']=='FAIL').sum()}

Reviewer Agreement : {agreement['agreement']:.2%}

Manual Review Queue : {len(review_df)}

Generated automatically.
"""

    Path(output).write_text(
        report,
        encoding="utf-8",
    )


if __name__ == "__main__":
    generate_report(
        validation_file="reports/validation_report.json",
        agreement_file="reports/agreement_summary.json",
        review_file="reports/review_queue.csv",
        output_file="reports/annotation_report.md"
    )
