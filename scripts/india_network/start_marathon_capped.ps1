# Capped marathon: full 120 fetch + marathon until deadline, NO incremental 05b while user works.
# Uses ~30% RAM cap, slower API pacing, final assemble only at 120/120.
#
#   powershell -ExecutionPolicy Bypass -File scripts\india_network\start_marathon_capped.ps1

param([int]$MaxHours = 10)

$ErrorActionPreference = "Continue"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root

Write-Host "=== Capped marathon (fetch now, assemble at end only) ===" -ForegroundColor Cyan

Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match 'overnight_supervisor|05b_assemble|06_build_domestic' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

Start-Sleep -Seconds 2

$env:INDIA_ETL_MEMORY = "low"
$env:ETL_RAM_CAP_MB = "3584"
$env:RESOURCE_CAP = "active"
$env:OPENALEX_FETCH_DELAY = "0.35"

Start-Process python -ArgumentList @(
    "scripts/india_network/overnight_supervisor.py",
    "--hours", $MaxHours,
    "--memory", "low",
    "--full-master",
    "--marathon",
    "--cap-resources",
    "--pipeline-sec", "3600",
    "--watch-sec", "600"
) -WorkingDirectory $Root -WindowStyle Hidden

Write-Host "Supervisor started (cap_resources=active, RAM cap 3.5GB for ETL steps)" -ForegroundColor Green
Write-Host "Fetch resumes from cache. Heavy 05b/06 only when 120/120 complete."
Write-Host "Log: data\logs\supervisor.log"
