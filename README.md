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

This repository intentionally **does not include industrial equipment images**.

Users should provide their own images inside:

```
data/images/
```

Supported formats:

- JPG
- JPEG
- PNG

Example equipment:

- Air Compressor
- Pump
- Valve
- Motor
- Bearing
- Gearbox
- Pipeline
- Heat Exchanger
- Electrical Panel

The benchmark uses `data/images.csv` to map metadata to each image.

Example:

```
IMG001_air_compressor.jpg
IMG002_pump.jpg
IMG003_valve.jpg
```

Image documentation:

- `data/images/README.md`
- `data/images/LICENSE_IMAGES.md`


## Local Execution

## Copy repository locally

```
git clone https://github.com/Enterprise-AI-Soutions/Industrial-Equipment-Image-Annotation-QA-Benchmark.git

cd Industrial-Equipment-Image-Annotation-QA-Benchmark.git

```

Create virtual environment

```
powershell-
py -3.12 -m venv .venv
.\.venv\Scripts\Activate

```

```
Vscode-
python -m venv .venv
Create virtual environment in vscode upon popup asking

```

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python -c "import pandas,numpy,pydantic,pytest; print('Environment OK')"

python -m src.validate_annotations `
data/annotations/annotator_1.json or python -m src.validate_annotations data/annotations/annotator_1.json

python -m src.agreement_analysis `
data/annotations/annotator_1.json `
data/annotations/annotator_2.json or python -m src.agreement_analysis data/annotations/annotator_1.json data/annotations/annotator_2.json


python -m src.create_review_queue `
data/annotations/annotator_1.json `
data/annotations/annotator_2.json `
reports/review_queue.csv or python -m src.create_review_queue data/annotations/annotator_1.json data/annotations/annotator_2.json reports/review_queue.csv

python -m src.generate_report

python -m pytest -q

```
powershell - .\scripts\run_pipeline.ps1
```
```
Vscode - chmod +x scripts/run_pipeline.sh
         ./scripts/run_pipeline.sh
```

```

## Output Screenshots

## Pipeline Execution

![Successful_Pipeline_Execution](docs/images/Pipeline_Success_vscode.png)

## Agreement Analysis

![agreement_Analysis](docs/images/Agreement_Summary_vscode.png)

## Review Queue

![Review_Queue](docs/images/Review_Queue_vscode.png)

## Report Generation

![Report_Generation](docs/images/Report_Generation_vscode.png)

## Validate Annotations

![Validate Annotations](docs/images/Validate_Annotations_vscode.png)
