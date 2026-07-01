# Overnight automation for 12 GB RAM laptops - max ~4.6 GB ETL RAM, full 120 fetch, NIRF PDF scrape.
# Run once before sleep (charger + disable sleep).
#
#   powershell -ExecutionPolicy Bypass -File scripts\india_network\start_overnight_safe.ps1

param([int]$MaxHours = 8)

$ErrorActionPreference = "Stop"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root

Write-Host "=== Overnight SAFE (12GB laptop, RAM cap ~40%) ===" -ForegroundColor Cyan

if (-not (Test-Path (Join-Path $Root ".env"))) {
    Write-Host "ABORT: .env missing" -ForegroundColor Red
    exit 1
}

$freeGb = [math]::Round((Get-PSDrive C).Free / 1GB, 1)
Write-Host "Disk free: ${freeGb} GB"
if ($freeGb -lt 6) {
    Write-Host "WARN: less than 6 GB free - cache growth may fail" -ForegroundColor Yellow
}

python scripts/india_network/check_openalex_key.py 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { exit 1 }

powershell -ExecutionPolicy Bypass -File scripts\india_network\checkpoint_data.ps1 -Label "pre_overnight"

Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match '05b_assemble|overnight_supervisor|05_fetch' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

Start-Sleep -Seconds 2

$env:INDIA_ETL_MEMORY = "low"
$env:ETL_RAM_CAP_MB = "4608"

Write-Host "Starting supervisor: full-master fetch, low-RAM assemble, NIRF PDF funding scrape" -ForegroundColor Green

Start-Process python -ArgumentList @(
    "scripts/india_network/overnight_supervisor.py",
    "--hours", $MaxHours,
    "--memory", "low",
    "--full-master",
    "--pipeline-sec", "3600",
    "--watch-sec", "300"
) -WorkingDirectory $Root -WindowStyle Hidden

Start-Sleep -Seconds 2
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File scripts\india_network\watchdog.ps1 -MaxHours $($MaxHours + 1)" -WorkingDirectory $Root -WindowStyle Hidden

Write-Host "Running. Logs: data\logs\supervisor.log"
Write-Host "Morning: powershell -File scripts\india_network\morning_report.ps1"
