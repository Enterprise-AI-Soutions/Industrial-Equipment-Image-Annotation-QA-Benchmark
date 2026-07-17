# ============================================================
#  Industrial Equipment Annotation QA — Easy Launcher
#  Run this from ANYWHERE:  & "E:\.gemini\Industrial-Equipment-Annotation\run.ps1"
# ============================================================

$ProjectRoot = "E:\.gemini\Industrial-Equipment-Annotation"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Industrial Equipment Image Annotation QA Benchmark" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Project : $ProjectRoot" -ForegroundColor Gray
Write-Host ""

# Navigate to project root so all relative paths work
Set-Location $ProjectRoot

# Run the pipeline script with bypass execution policy
& powershell.exe -ExecutionPolicy Bypass -File "$ProjectRoot\scripts\run_pipeline.ps1"
