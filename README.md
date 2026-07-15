# Industrial Equipment Image Annotation QA Benchmark

A lightweight benchmark demonstrating a complete Image Annotation Quality Assurance workflow for industrial equipment datasets.

This repository simulates a production annotation review pipeline used by AI data companies.

---

## Project Objectives

This benchmark demonstrates:

- Image metadata validation
- Annotation schema validation
- Bounding-box quality checks
- Duplicate annotation detection
- Annotation agreement analysis
- IoU (Intersection over Union) scoring
- Review queue generation
- Quality reporting

The project is intentionally lightweight while showcasing practical annotation QA skills.

---

# Repository Structure

Industrial-Equipment-Image-Annotation-QA-Benchmark/

data/

images.csv

annotator_1.jsonl

annotator_2.jsonl

dataimages/

LICENSE_IMAGES.md

README.md

reports/

agreement_summary.json

annotation_report.md

annotation_summary.csv

duplicate_boxes.csv

review_queue.csv

rubrics/

annotation_rubric.json

scripts/

run_pipeline.ps1

run_pipeline.sh

src/

validate_annotations.py

calculate_iou.py

duplicate_detection.py

agreement_analysis.py

quality_scoring.py

create_review_queue.py

generate_report.py

schemas.py

tests/

test_iou.py

test_scoring.py

test_validation.py

.gitignore

LICENSE

README.md

pyproject.toml

requirements.txt

---

## Technologies

- Python 3.12
- Pandas
- NumPy
- Pydantic
- JSON
- Pytest

---
## Dataset

The benchmark includes a small industrial equipment image dataset located in:

```
data/images/
```

Image sources and licensing information are available in:

- `data/images/README.md`
- `data/images/LICENSE_IMAGES.md`


## Local Installation

Create virtual environment

```powershell
py -3.12 -m venv .venv

.venv\Scripts\activate

# Output Screenshots

docs/images/

pipeline_execution.png

agreement_summary.png

review_queue.png

report_generation.png
