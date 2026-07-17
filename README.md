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

```
Industrial-Equipment-Image-Annotation-QA-Benchmark/
├── data/
│   ├── annotations/
│   │   ├── annotator_1.json
│   │   ├── annotator_2.json
│   │   └── ground_truth.json
│   ├── images/               ← Upload your 9 images here
│   └── images.csv
├── reports/
│   ├── agreement_summary.json
│   ├── annotation_report.md
│   ├── annotation_summary.csv
│   ├── duplicate_boxes.csv
│   ├── review_queue.csv
│   └── validation_report.json
├── rubrics/
│   └── annotation_rubric.json
├── scripts/
│   ├── run_pipeline.ps1
│   └── run_pipeline.sh
├── src/
│   ├── validate_annotations.py
│   ├── calculate_iou.py
│   ├── duplicate_detection.py
│   ├── agreement_analysis.py
│   ├── quality_scoring.py
│   ├── create_review_queue.py
│   ├── generate_report.py
│   ├── schemas.py
│   └── config.py
├── tests/
│   ├── test_iou.py
│   ├── test_scoring.py
│   ├── test_validation.py
│   └── test_duplicates.py
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
└── requirements.txt
```

---

## Technologies

- Python 3.12
- Pandas
- NumPy
- Pydantic
- JSON
- Pytest

---

## ⚠️ Mandatory: Upload Your Images First

> **This pipeline will NOT run without images.**
>
> You must upload exactly **9 industrial equipment images** into `data/images/` before running any pipeline step.
> The pipeline includes a pre-flight check and will exit with an error if no images are found.

**Required image filenames** (JPG / JPEG / PNG):

```
data/images/pump.jpg
data/images/valve.jpg
data/images/motor.jpg
data/images/bearing.jpg
data/images/pipeline.jpg
data/images/gearbox.jpg
data/images/air_compressor.jpg
data/images/heat_exchanger.jpg
data/images/electrical_panel.jpg
```

Images are **tracked by git** (not gitignored) — every user who clones this repository must add their own images.

---

## Local Execution

### 1. Clone the repository

```powershell
git clone https://github.com/Enterprise-AI-Soutions/Industrial-Equipment-Image-Annotation-QA-Benchmark.git
cd Industrial-Equipment-Image-Annotation-QA-Benchmark
```

### 2. Upload your 9 images

Copy your industrial equipment images into `data/images/` (see filenames above).

### 3. Create virtual environment

**PowerShell:**
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate
```

**VSCode / bash:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -c "import pandas,numpy,pydantic,pytest; print('Environment OK')"
```

### 5. Run the full pipeline (recommended)

```powershell
.\scripts\run_pipeline.ps1
```

This runs all 6 steps in order:
1. ✔ Validate annotations (with image existence check)
2. ✔ Duplicate bounding box detection
3. ✔ Reviewer agreement analysis (label + IoU)
4. ✔ Review queue generation
5. ✔ Consolidated report generation
6. ✔ Unit tests

### 6. Or run individual steps

```powershell
# Step 1 — Validate annotations
python -m src.validate_annotations data/annotations/annotator_1.json

# Step 2 — Reviewer agreement
python -m src.agreement_analysis data/annotations/annotator_1.json data/annotations/annotator_2.json

# Step 3 — Review queue
python -m src.create_review_queue data/annotations/annotator_1.json data/annotations/annotator_2.json reports/review_queue.csv

# Step 4 — Generate report
python -m src.generate_report

# Run tests only
python -m pytest -v
```

---

## Output Files

After a successful pipeline run, the following files are generated in `reports/`:

| File | Description |
|------|-------------|
| `validation_report.json` | Schema + class validation results |
| `agreement_summary.json` | Inter-annotator label + IoU agreement |
| `review_queue.csv` | Annotations flagged for manual review |
| `duplicate_boxes.csv` | Near-duplicate bounding box pairs |
| `annotation_summary.csv` | Per-image annotation overview |
| `annotation_report.md` | Consolidated Markdown QA report |

---

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
