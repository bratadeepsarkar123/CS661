# =============================================================================
# OVERNIGHT START — run this ONCE right before you close the lid / go to sleep.
# Do NOT run while you are still using the laptop.
#
#   cd C:\Users\brata\Downloads\CS661
#   powershell -ExecutionPolicy Bypass -File scripts\india_network\start_overnight.ps1
#
# Keeps going up to 8 hours. Logs in data\logs\
# Morning summary: powershell -File scripts\india_network\morning_report.ps1
# =============================================================================

param(
    [int]$MaxHours = 8
)

$ErrorActionPreference = "Stop"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root

$LogDir = Join-Path $Root "data\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$StartedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$StartLog = Join-Path $LogDir "overnight_started.txt"

function Fail($msg) {
    Write-Host "ABORT: $msg" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== CS661 Module 5 — Overnight automation ===" -ForegroundColor Cyan
Write-Host ""

# --- Preflight ---
if (-not (Test-Path (Join-Path $Root ".env"))) {
    Fail ".env missing. Copy .env.example -> .env and paste your OpenAlex API key first."
}

$freeGb = [math]::Round((Get-PSDrive C).Free / 1GB, 1)
Write-Host "Disk free: ${freeGb} GB"
if ($freeGb -lt 8) {
    Fail "Less than 8 GB free — free space first or cache growth will hang the laptop."
}

Write-Host "Checking API key..."
python scripts/india_network/check_openalex_key.py 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Fail "OpenAlex API key check failed. Fix .env then retry."
}
Write-Host "API key OK." -ForegroundColor Green

# Kill stray old fetch processes (avoid duplicates after reboot)
Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match "05_fetch_openalex_works" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

Write-Host ""
Write-Host "Preflight passed. Starting orchestrator for ${MaxHours} hours..." -ForegroundColor Green
Write-Host "  Logs:  data\logs\nightly_orchestrator.log"
Write-Host "  Watch: data\logs\openalex_watch.log"
Write-Host ""
Write-Host "TIP: Set power plan to 'Never sleep' when plugged in, or keep charger connected."
Write-Host ""

@(
    "started_at=$StartedAt"
    "max_hours=$MaxHours"
    "disk_free_gb=$freeGb"
    "supervisor=overnight_supervisor.py"
) | Set-Content $StartLog

Write-Host "Starting resilient Python supervisor + watchdog (memory=high)..." -ForegroundColor Green

$env:INDIA_ETL_MEMORY = "high"
Start-Process python -ArgumentList "scripts/india_network/overnight_supervisor.py --hours $MaxHours --memory high" `
    -WorkingDirectory $Root -WindowStyle Hidden

Start-Sleep -Seconds 3

Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File scripts\india_network\watchdog.ps1 -MaxHours $($MaxHours + 1)" `
    -WorkingDirectory $Root -WindowStyle Hidden

Write-Host "Supervisor + watchdog running in background." -ForegroundColor Green
Write-Host "  Main log:  data\logs\supervisor.log"
Write-Host "  Watchdog:  data\logs\watchdog.log"
Write-Host ""
Write-Host "You can close this window — processes keep running."
Write-Host "Morning: powershell -ExecutionPolicy Bypass -File scripts\india_network\morning_report.ps1"
