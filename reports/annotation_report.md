# Industrial Equipment Image Annotation QA Benchmark

Generated: 2026-07-18 00:24:32

---

## Validation Results

| Metric                      | Value         |
|-----------------------------|---------------|
| Images Reviewed             | 9  |
| Annotations Validated       | 9 |
| Schema Errors               | 0  |
| Image Validation Issues     | 0  |
| Overall Status              | PASSED  |

---

## Per-Image Validation (Actual Image Files)

| Image ID | Resolved Filename             | Width   | Height  | Label                | BBox                   | BBox Status     |
|----------|-------------------------------|---------|---------|----------------------|------------------------|-----------------|
| IMG001   | pump_001.png                 |    2500 |    2500 | pump                 | [120, 85, 220, 165]    | [OK]            |
| IMG002   | valve_001.jpg                |     740 |     493 | valve                | [320, 105, 92, 88]     | [OK]            |
| IMG003   | motor_001.jpg                |     612 |     459 | motor                | [60, 140, 185, 170]    | [OK]            |
| IMG004   | bearing_001.jpg              |     612 |     407 | bearing              | [180, 160, 80, 80]     | [OK]            |
| IMG005   | pipeline_001.jpg             |    2940 |    1960 | pipeline             | [40, 210, 430, 55]     | [OK]            |
| IMG006   | gearbox_001.jpg              |     740 |     740 | gearbox              | [145, 110, 170, 130]   | [OK]            |
| IMG007   | air_compressor_001.png       |     664 |     650 | compressor           | [90, 90, 240, 180]     | [OK]            |
| IMG008   | heat_exchanger_001.jpg       |     523 |     360 | heat exchanger       | [170, 95, 260, 170]    | [OK]            |
| IMG009   | electrical_panel_001.jpg     |    1749 |     980 | electrical panel     | [125, 75, 185, 245]    | [OK]            |


All images resolved and bounding boxes validated successfully.


---

## Reviewer Agreement

| Metric              | Value         |
|---------------------|---------------|
| Label Agreement     | 100.0% |
| Mean IoU            | 0.973 |
| Matching Labels     | 9 / 9 |

### Per-Label Breakdown

| Label                  | Count | Label Agreement  | Mean IoU |
|------------------------|-------|------------------|----------|
| pump                   |     1 |           100.0% |    0.972 |
| valve                  |     1 |           100.0% |    0.967 |
| motor                  |     1 |           100.0% |    0.978 |
| bearing                |     1 |           100.0% |    0.975 |
| pipeline               |     1 |           100.0% |    0.941 |
| gearbox                |     1 |           100.0% |    0.981 |
| compressor             |     1 |           100.0% |    0.977 |
| heat exchanger         |     1 |           100.0% |    0.971 |
| electrical panel       |     1 |           100.0% |    0.991 |

---

## Duplicate Detection

Near-duplicate bounding boxes detected (IoU >= threshold): **0**

---

## Review Queue

Annotations flagged for manual review: **0**


---

## Output Files

| File                            | Description                             |
|---------------------------------|-----------------------------------------|
| reports/validation_report.json  | Schema + image + class validation       |
| reports/agreement_summary.json  | Inter-annotator label + IoU agreement   |
| reports/review_queue.csv        | Annotations flagged for review          |
| reports/duplicate_boxes.csv     | Near-duplicate bounding boxes           |
| reports/annotation_summary.csv  | Per-image: real dims, bbox status       |

---

*Generated automatically by Industrial Equipment Image Annotation QA Benchmark.*
