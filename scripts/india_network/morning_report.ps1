# Morning summary — run after waking up.
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CS661 Module 5 — Morning Report" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$LogDir = Join-Path $Root "data\logs"
if (Test-Path (Join-Path $LogDir "overnight_started.txt")) {
    Write-Host "--- Overnight run ---" -ForegroundColor Yellow
    Get-Content (Join-Path $LogDir "overnight_started.txt")
    if (Test-Path (Join-Path $LogDir "overnight_finished.txt")) {
        Get-Content (Join-Path $LogDir "overnight_finished.txt")
    } else {
        Write-Host "  (orchestrator may still be running or was interrupted)"
    }
    Write-Host ""
}

Write-Host "--- OpenAlex fetch progress ---" -ForegroundColor Yellow
python scripts/india_network/openalex_progress.py --full-master

Write-Host ""
Write-Host "--- Feasibility gate ---" -ForegroundColor Yellow
if (Test-Path "data\processed\feasibility_report.md") {
    Get-Content "data\processed\feasibility_report.md"
} else {
    Write-Host "  (not generated yet)"
}

Write-Host ""
Write-Host "--- Dashboard payloads ---" -ForegroundColor Yellow
Get-ChildItem dashboard\data\india_network\*.json -ErrorAction SilentlyContinue |
    Format-Table Name, @{N='KB';E={[math]::Round($_.Length/1KB,1)}}, LastWriteTime

Write-Host ""
Write-Host "--- Disk ---" -ForegroundColor Yellow
$free = [math]::Round((Get-PSDrive C).Free / 1GB, 1)
Write-Host "  Free: ${free} GB"

Write-Host ""
Write-Host "--- Supervisor status ---" -ForegroundColor Yellow
if (Test-Path "data\logs\supervisor_status.json") {
    Get-Content "data\logs\supervisor_status.json"
} else {
    Write-Host "  (supervisor not started or no status yet)"
}

Write-Host ""
Write-Host "--- Last supervisor log lines ---" -ForegroundColor Yellow
if (Test-Path "data\logs\supervisor.log") {
    Get-Content "data\logs\supervisor.log" -Tail 15
}
Write-Host "  1. If institutions < 30/30: re-run start_overnight.ps1 tonight OR wait for API budget"
Write-Host "  2. NIRF patents (optional funding tab): paid Dataful — skip for v1"
Write-Host "  3. Test dashboard: cd dashboard; python -m http.server 8765"
Write-Host "  4. Open http://localhost:8765 and click Module 5 panel"
Write-Host ""
Write-Host "Full logs: data\logs\nightly_orchestrator.log"
Write-Host ""
