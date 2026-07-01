# Switch to laptop-friendly mode: stop heavy 05b, keep OpenAlex cache, resume fetch only.
# Usage: powershell -ExecutionPolicy Bypass -File scripts\india_network\laptop_mode.ps1

$ErrorActionPreference = "Continue"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root
$LogDir = Join-Path $Root "data\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Log = Join-Path $LogDir "laptop_mode.log"

function Log($m) {
    $l = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $m"
    Write-Host $l
    Add-Content $Log $l
}

Log "=== Laptop mode: stop heavy ETL, preserve cache ==="

# Stop heavy assemble + old supervisors (NOT the viz server on 8766)
Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object {
        $_.CommandLine -match '05b_assemble|overnight_supervisor|agent_monitor_loop|06_build_domestic'
    } |
    ForEach-Object {
        Log "Stopping PID $($_.ProcessId): $($_.CommandLine.Substring(0, [Math]::Min(80, $_.CommandLine.Length)))..."
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }

Start-Sleep -Seconds 2

# Remove incomplete parquet from interrupted 05b (edges/dashboard JSON from last good run remain)
foreach ($f in @(
        "data\processed\works_raw.parquet.tmp",
        "data\processed\works_raw.parquet",
        "data\processed\_works_assemble_dedup.sqlite"
    )) {
    $p = Join-Path $Root $f
    if (Test-Path $p) {
        Remove-Item $p -Force
        Log "Removed incomplete: $f"
    }
}

$cache = Get-ChildItem (Join-Path $Root "data\cache\openalex\works_*.json") -ErrorAction SilentlyContinue
$cacheCount = $cache.Count
$statePath = Join-Path $Root "data\logs\pipeline_state.json"
$state = @{
    updated_at = (Get-Date).ToUniversalTime().ToString("o")
    cache_at_last_heavy = $cacheCount
}
$state | ConvertTo-Json | Set-Content $statePath -Encoding UTF8
Log "Pipeline state: cache_at_last_heavy=$cacheCount (prevents 05b until +400 new pages or overnight)"
Log "OpenAlex cache preserved: $cacheCount files (~$([math]::Round(($cache | Measure-Object Length -Sum).Sum/1GB, 2)) GB)"

$env:INDIA_ETL_MEMORY = "low"

$fetchRunning = Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match '05_fetch_openalex_works' }
if (-not $fetchRunning) {
    Log "Starting lightweight fetch (05) — resumes from cache, no re-download of cached pages"
    Start-Process python -ArgumentList "scripts/india_network/05_fetch_openalex_works.py --pilot-top 30" `
        -WorkingDirectory $Root -WindowStyle Hidden
} else {
    Log "Fetch already running — left untouched"
}

Log "Starting supervisor (memory=low, skips 05b unless cache +400 new files)"
Start-Process python -ArgumentList "scripts/india_network/overnight_supervisor.py --hours 4 --pipeline-sec 1800 --memory low" `
    -WorkingDirectory $Root -WindowStyle Hidden

Log "Done. Dashboard: cd dashboard; python -m http.server 8766"
Log "Overnight assemble: powershell -File scripts\india_network\start_overnight.ps1"
