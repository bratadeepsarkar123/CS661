# Finish remaining 4 institutions + monitor + auto-pipeline when done.
# Usage: powershell -ExecutionPolicy Bypass -File scripts\india_network\finish_fetch.ps1

$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root
$LogDir = Join-Path $Root "data\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Log($m) {
    $l = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $m"
    Write-Host $l
    Add-Content (Join-Path $LogDir "finish_fetch.log") $l
}

Log "=== Finish fetch started ==="

# Single fetch process
Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match '05_fetch_openalex_works|overnight_supervisor|agent_monitor' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

Start-Sleep -Seconds 2

Log "Starting fetch (05) for pilot-top 30..."
Start-Process python -ArgumentList "scripts/india_network/05_fetch_openalex_works.py --pilot-top 30" `
    -WorkingDirectory $Root -WindowStyle Hidden

Log "Starting agent monitor (4h max)..."
Start-Process python -ArgumentList "scripts/india_network/agent_monitor_loop.py --hours 4 --interval 300" `
    -WorkingDirectory $Root -WindowStyle Hidden

Log "Starting lightweight supervisor (4h, memory=low)..."
Start-Process python -ArgumentList "scripts/india_network/overnight_supervisor.py --hours 4 --pipeline-sec 1800 --memory low" `
    -WorkingDirectory $Root -WindowStyle Hidden

Log "All three layers running. Tail: data\logs\agent_monitor.log"
