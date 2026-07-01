# Graceful pause before shutdown — preserves cache, saves checkpoint + resume instructions.
# Usage: powershell -ExecutionPolicy Bypass -File scripts\india_network\pause_gracefully.ps1

$ErrorActionPreference = "Continue"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root
$LogDir = Join-Path $Root "data\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$PauseLog = Join-Path $LogDir "pause_graceful.log"

function Log($m) {
    $l = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $m"
    Write-Host $l
    Add-Content $PauseLog $l
}

Log "=== Graceful pause started ==="

# 1) Stop fetch first (let current HTTP response finish)
$fetch = Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match '05_fetch_openalex_works' }
if ($fetch) {
    Log "Stopping fetch (waiting 3s for in-flight page write)..."
    Start-Sleep -Seconds 3
    $fetch | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
}

# 2) Stop assemble/edges if any
Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match '05b_assemble|06_build_domestic|validate_openalex' } |
    ForEach-Object {
        Log "Stopping PID $($_.ProcessId) ($($_.CommandLine.Substring(0,60))...)"
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }

Start-Sleep -Seconds 2

# 3) Stop supervisor last
Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match 'overnight_supervisor|agent_monitor' } |
    ForEach-Object {
        Log "Stopping supervisor PID $($_.ProcessId)"
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }

Start-Sleep -Seconds 1

# 4) Clean only incomplete temp files (keep complete parquet + cache)
foreach ($f in @(
        "data\processed\works_raw.parquet.tmp",
        "data\processed\_works_assemble_dedup.sqlite-shm",
        "data\processed\_works_assemble_dedup.sqlite-wal"
    )) {
    $p = Join-Path $Root $f
    if (Test-Path $p) {
        Remove-Item $p -Force -ErrorAction SilentlyContinue
        Log "Removed temp: $f"
    }
}

# If works_raw is corrupt (no footer), remove so resume rebuilds cleanly
$wr = Join-Path $Root "data\processed\works_raw.parquet"
if (Test-Path $wr) {
    try {
        python -c "import pyarrow.parquet as pq; pq.read_metadata(r'$wr')" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Remove-Item $wr -Force
            Log "Removed corrupt works_raw.parquet"
        } else {
            Log "works_raw.parquet OK — kept"
        }
    } catch {
        Log "works_raw check skipped"
    }
}

# 5) Save pipeline state (cache count baseline)
$cacheCount = (Get-ChildItem (Join-Path $Root "data\cache\openalex\works_*.json") -ErrorAction SilentlyContinue).Count
$statePath = Join-Path $LogDir "pipeline_state.json"
@{
    updated_at = (Get-Date).ToUniversalTime().ToString("o")
    cache_at_last_heavy = $cacheCount
    paused = $true
} | ConvertTo-Json | Set-Content $statePath -Encoding UTF8
Log "pipeline_state: cache_at_last_heavy=$cacheCount paused=true"

# 6) Progress snapshot
$progressOut = python scripts/india_network/openalex_progress.py --full-master 2>&1 | Out-String
Log "Progress snapshot:"
$progressOut -split "`n" | Select-Object -Last 5 | ForEach-Object { Log "  $_" }

# 7) Checkpoint processed/raw/dashboard (NOT 6GB cache — too slow on battery)
Log "Checkpoint (processed + raw + dashboard only)..."
powershell -ExecutionPolicy Bypass -File scripts\india_network\checkpoint_data.ps1 -Label "graceful_pause"

# 8) Resume instructions
$resume = @"
# Module 5 — PAUSED (safe to shut down laptop)

Paused at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
OpenAlex cache files: $cacheCount (on disk — NOT lost on shutdown)
Checkpoint: see data/checkpoints/LATEST.json

## After restart — resume capped marathon (low RAM while you work):
``````powershell
cd C:\Users\brata\Downloads\CS661
powershell -ExecutionPolicy Bypass -File scripts\india_network\start_marathon_capped.ps1
``````

## Or light fetch only:
``````powershell
powershell -ExecutionPolicy Bypass -File scripts\india_network\laptop_mode.ps1
``````

Fetch never re-downloads cached pages. All progress is in data/cache/openalex/.
"@

$resume | Set-Content (Join-Path $LogDir "PAUSED_README.md") -Encoding UTF8
@{
    paused_at = (Get-Date).ToUniversalTime().ToString("o")
    cache_files = $cacheCount
    resume_script = "scripts/india_network/start_marathon_capped.ps1"
    checkpoint = (Get-Content (Join-Path $Root "data\checkpoints\LATEST.json") -Raw | ConvertFrom-Json).checkpoint
} | ConvertTo-Json | Set-Content (Join-Path $LogDir "PAUSED.json") -Encoding UTF8

# Supervisor status
@{
    updated_at = (Get-Date).ToUniversalTime().ToString("o")
    state = "paused_graceful"
    cache_files = $cacheCount
} | ConvertTo-Json | Set-Content (Join-Path $LogDir "supervisor_status.json") -Encoding UTF8

Log "=== PAUSE COMPLETE — safe to shut down ==="
Log "Resume: data\logs\PAUSED_README.md"
