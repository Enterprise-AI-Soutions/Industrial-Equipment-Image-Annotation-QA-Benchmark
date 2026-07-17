$ErrorActionPreference = "Stop"

# Always run from the project root directory (works from any location)
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
$env:PYTHONPATH = $ProjectRoot

# Only use the project's own .venv — no fallbacks to system or user Python
if (Test-Path "$ProjectRoot\.venv\Scripts\python.exe") {
    $Python = "$ProjectRoot\.venv\Scripts\python.exe"
} else {
    Write-Host ""
    Write-Host "[ERROR] Project virtual environment not found." -ForegroundColor Red
    Write-Host "Please run the following from the project directory:" -ForegroundColor Yellow
    Write-Host "  py -3.12 -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate" -ForegroundColor Yellow
    Write-Host "  python -m pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "Working directory : $ProjectRoot" -ForegroundColor Cyan
Write-Host "Python executable : $Python" -ForegroundColor Cyan
Write-Host "PYTHONPATH set to : $ProjectRoot" -ForegroundColor Cyan

function Run-Step {

    param(

        [string]$Title,

        [scriptblock]$Command

    )

    Write-Host ""
    Write-Host "==============================================="
    Write-Host $Title
    Write-Host "==============================================="
    Write-Host ""

    & $Command

    if ($LASTEXITCODE -ne 0){

        Write-Error "Pipeline failed at: $Title"

        exit $LASTEXITCODE

    }

}

Write-Host ""
Write-Host "============================================================"
Write-Host " Industrial Equipment Image Annotation QA Benchmark"
Write-Host "============================================================"
Write-Host ""

# ---------------------------------------------------------
# Pre-flight check: Ensure images exist in data/images/
# ---------------------------------------------------------
$imageFiles = @(
    Get-ChildItem -Path "data\images\*.jpg"  -ErrorAction SilentlyContinue
    Get-ChildItem -Path "data\images\*.jpeg" -ErrorAction SilentlyContinue
    Get-ChildItem -Path "data\images\*.png"  -ErrorAction SilentlyContinue
)

if ($imageFiles.Count -eq 0) {
    Write-Host ""
    Write-Host "[ERROR] No images found in data/images/" -ForegroundColor Red
    Write-Host "Please upload your 9 industrial equipment images (JPG/JPEG/PNG) to data/images/ before running this pipeline." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "  Found $($imageFiles.Count) image(s) in data/images/ [OK]" -ForegroundColor Green
Write-Host ""

# ---------------------------------------------------------
# Step 1 — Validate Annotation File
# ---------------------------------------------------------
Run-Step "Step 1 - Validate Annotation File" {

    & $Python -m src.validate_annotations `
    data/annotations/annotator_1.json

}

# ---------------------------------------------------------
# Step 2 — Duplicate Box Detection
# ---------------------------------------------------------
Run-Step "Step 2 - Duplicate Bounding Box Detection" {

    & $Python -c "
import json
from src.validate_annotations import validate_annotations
from src.duplicate_detection import find_duplicate_boxes, write_duplicate_report

anns, _ = validate_annotations('data/annotations/annotator_1.json')
dups = find_duplicate_boxes(anns)
out = write_duplicate_report(dups)
print(f'  Found {len(dups)} duplicate bounding box pair(s).')
print(f'  Written to: {out}')
"

}

# ---------------------------------------------------------
# Step 3 — Reviewer Agreement
# ---------------------------------------------------------
Run-Step "Step 3 - Reviewer Agreement" {

    & $Python -m src.agreement_analysis `
    data/annotations/annotator_1.json `
    data/annotations/annotator_2.json

}

# ---------------------------------------------------------
# Step 4 — Review Queue
# ---------------------------------------------------------
Run-Step "Step 4 - Review Queue" {

    & $Python -m src.create_review_queue `
    data/annotations/annotator_1.json `
    data/annotations/annotator_2.json `
    reports/review_queue.csv

}

# ---------------------------------------------------------
# Step 5 — Generate Report (depends on all above outputs)
# ---------------------------------------------------------
Run-Step "Step 5 - Generate Report" {

    & $Python -m src.generate_report

}

# ---------------------------------------------------------
# Step 6 — Unit Tests
# ---------------------------------------------------------
Run-Step "Step 6 - Unit Tests" {

    & $Python -m pytest "$ProjectRoot\tests" -v

}

Write-Host ""
Write-Host "============================================================"
Write-Host " Pipeline completed successfully."
Write-Host "============================================================"
Write-Host ""
Write-Host " Output files:"
Write-Host "   reports/validation_report.json"
Write-Host "   reports/agreement_summary.json"
Write-Host "   reports/review_queue.csv"
Write-Host "   reports/duplicate_boxes.csv"
Write-Host "   reports/annotation_summary.csv"
Write-Host "   reports/annotation_report.md"
Write-Host ""
