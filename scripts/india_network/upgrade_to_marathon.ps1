# Upgrade running overnight job to marathon mode (keep fetch alive).
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root

Write-Host "Upgrading to MARATHON mode (10h, RAM cap 7GB, no early exit)" -ForegroundColor Cyan

Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match 'overnight_supervisor' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

Start-Sleep -Seconds 2

$env:INDIA_ETL_MEMORY = "low"
$env:ETL_RAM_CAP_MB = "7168"

Start-Process python -ArgumentList @(
    "scripts/india_network/overnight_supervisor.py",
    "--hours", "10",
    "--memory", "low",
    "--full-master",
    "--marathon",
    "--pipeline-sec", "1800",
    "--watch-sec", "300"
) -WorkingDirectory $Root -WindowStyle Hidden

Write-Host "Marathon supervisor started. Fetch process left running." -ForegroundColor Green
