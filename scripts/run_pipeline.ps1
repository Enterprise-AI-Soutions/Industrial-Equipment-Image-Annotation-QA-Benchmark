Write-Host ""
Write-Host "Industrial Equipment Image Annotation QA Benchmark"
Write-Host "================================================="
Write-Host ""

python -m src.validate_annotations

python -m src.duplicate_detection

python -m src.agreement_analysis

python -m src.quality_scoring

python -m src.create_review_queue

python -m src.generate_report

Write-Host ""
Write-Host "Running Tests..."
python -m pytest -q

Write-Host ""
Write-Host "Pipeline completed successfully."
