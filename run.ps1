# ============================================================
#  Industrial Equipment Annotation QA — Easy Launcher
#  Run this from ANYWHERE:
#    powershell -ExecutionPolicy Bypass -File "E:\.gemini\Industrial-Equipment-Annotation\run.ps1"
# ============================================================

$ProjectRoot = "E:\.gemini\Industrial-Equipment-Annotation"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Industrial Equipment Image Annotation QA Benchmark" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Project : $ProjectRoot" -ForegroundColor Gray
Write-Host ""

# Verify the project .venv exists before launching
if (-not (Test-Path "$ProjectRoot\.venv\Scripts\python.exe")) {
    Write-Host "[ERROR] Project virtual environment not found at $ProjectRoot\.venv" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set up the environment first:" -ForegroundColor Yellow
    Write-Host "  cd $ProjectRoot" -ForegroundColor Yellow
    Write-Host "  py -3.12 -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate" -ForegroundColor Yellow
    Write-Host "  python -m pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Navigate to project root and run pipeline using project .venv only
Set-Location $ProjectRoot
& powershell.exe -ExecutionPolicy Bypass -File "$ProjectRoot\scripts\run_pipeline.ps1"
