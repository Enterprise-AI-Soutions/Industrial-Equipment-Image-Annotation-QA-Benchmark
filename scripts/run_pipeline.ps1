$ErrorActionPreference = "Stop"

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

        Write-Error "Pipeline failed."

        exit $LASTEXITCODE

    }

}

Write-Host ""
Write-Host "Industrial Equipment Image Annotation QA Benchmark"
Write-Host ""

Run-Step "Step 1 - Validate Annotation File" {

python -m src.validate_annotations `
data/annotations/annotator_1.json

}

Run-Step "Step 2 - Reviewer Agreement" {

python -m src.agreement_analysis `
data/annotations/annotator_1.json `
data/annotations/annotator_2.json

}

Run-Step "Step 3 - Review Queue" {

python -m src.create_review_queue `
data/annotations/annotator_1.json `
data/annotations/annotator_2.json `
reports/review_queue.csv

}

Run-Step "Step 4 - Generate Report" {

python -m src.generate_report

}

Step 5 - Unit Tests

Write-Host ""
Write-Host "==============================================="
Write-Host "Pipeline completed successfully."
Write-Host "==============================================="
