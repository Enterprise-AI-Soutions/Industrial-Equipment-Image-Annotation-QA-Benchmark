# Industrial Equipment Image Annotation QA Benchmark

Generated: 2026-07-17 20:03:42

---

## Validation Results

| Metric              | Value         |
|---------------------|---------------|
| Images Reviewed     | 9  |
| Annotations Parsed  | 9 |
| Issues Found        | 0  |
| Status              | PASSED  |

---

## Reviewer Agreement

| Metric              | Value         |
|---------------------|---------------|
| Label Agreement     | 100.0% |
| Mean IoU            | 0.973 |
| Matching Labels     | 9 / 9 |

### Per-Label Breakdown

| Label                | Count | Label Agreement  | Mean IoU |
|----------------------|-------|------------------|----------|
| pump                 |     1 |           100.0% |    0.972 |
| valve                |     1 |           100.0% |    0.967 |
| motor                |     1 |           100.0% |    0.978 |
| bearing              |     1 |           100.0% |    0.975 |
| pipeline             |     1 |           100.0% |    0.941 |
| gearbox              |     1 |           100.0% |    0.981 |
| compressor           |     1 |           100.0% |    0.977 |
| heat exchanger       |     1 |           100.0% |    0.971 |
| electrical panel     |     1 |           100.0% |    0.991 |

---

## Duplicate Detection

Near-duplicate bounding boxes detected (IoU >= threshold): **0**

---

## Review Queue

Annotations flagged for manual review: **0**


---

## Output Files

| File                            | Description                        |
|---------------------------------|------------------------------------|
| reports/validation_report.json  | Schema + class validation results  |
| reports/agreement_summary.json  | Inter-annotator agreement scores   |
| reports/review_queue.csv        | Annotations flagged for review     |
| reports/duplicate_boxes.csv     | Near-duplicate bounding boxes      |
| reports/annotation_summary.csv  | Per-image annotation overview      |

---

*Generated automatically by Industrial Equipment Image Annotation QA Benchmark.*
