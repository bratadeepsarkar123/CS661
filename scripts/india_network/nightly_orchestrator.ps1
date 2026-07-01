# Overnight automation — self-contained: starts OpenAlex fetch + periodic pipeline passes.
#
# Normally started via start_overnight.ps1 (run that before sleep, not this directly).

param(
    [int]$WatchIntervalSec = 300,
    [int]$PipelineIntervalSec = 1800,
    [int]$MaxHours = 8,
    [float]$StallMinutes = 20
)

$ErrorActionPreference = "Continue"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root

$LogDir = Join-Path $Root "data\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Log = Join-Path $LogDir "nightly_orchestrator.log"
$FetchLog = Join-Path $LogDir "openalex_fetch.log"

function Log($msg) {
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
    Write-Host $line
    Add-Content -Path $Log -Value $line -Encoding UTF8
}

function Get-PilotCompleteCount {
    $out = python scripts/india_network/openalex_progress.py --pilot-top 30 2>&1 | Out-String
    if ($out -match "Complete:\s*(\d+)/(\d+)") {
        return [int]$Matches[1], [int]$Matches[2]
    }
    return 0, 30
}

function Start-FetchProcess {
    Log "Launching lightweight OpenAlex fetch (05)"
    Start-Process -FilePath "python" `
        -ArgumentList "scripts/india_network/05_fetch_openalex_works.py --pilot-top 30" `
        -WorkingDirectory $Root -WindowStyle Hidden
}

function Fetch-IsRunning {
    Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -match "05_fetch_openalex_works" } |
        Select-Object -First 1
}

Log "=== Nightly orchestrator started (max ${MaxHours}h) ==="
Log "Watch every ${WatchIntervalSec}s | Pipeline every ${PipelineIntervalSec}s | Stall=${StallMinutes}min"

$deadline = (Get-Date).AddHours($MaxHours)
$lastPipeline = [datetime]::MinValue
$lastCacheCount = -1
$stallSince = $null
$fetchProc = $null

# Initial fetch
if (-not (Fetch-IsRunning)) {
    $fetchProc = Start-FetchProcess
} else {
    Log "Fetch already running — attaching monitor only."
}

# First pipeline pass soon (refresh dashboard with current cache)
Log "Initial pipeline pass (assemble + filter + export from current cache)..."
& "$PSScriptRoot\run_pipeline.ps1" 2>&1 | ForEach-Object { Log "pipeline: $_" }
$lastPipeline = Get-Date

while ((Get-Date) -lt $deadline) {
    # --- Watch cache ---
    python scripts/india_network/watch_openalex_fetch.py --stall-minutes $StallMinutes 2>&1 |
        ForEach-Object { Log "watch: $_" }

    $statusPath = Join-Path $LogDir "openalex_watch_status.json"
    if (Test-Path $statusPath) {
        $status = Get-Content $statusPath -Raw | ConvertFrom-Json
        $count = [int]$status.cache_files
        if ($count -eq $lastCacheCount) {
            if (-not $stallSince) { $stallSince = Get-Date }
        } else {
            $stallSince = $null
            $lastCacheCount = $count
        }
    }

    $done, $total = Get-PilotCompleteCount
    Log "Progress: $done/$total institutions fully cached | cache files=$lastCacheCount"

    if ($done -ge $total) {
        Log "All $total pilot institutions cached. Final pipeline pass..."
        & "$PSScriptRoot\run_pipeline.ps1" 2>&1 | ForEach-Object { Log "pipeline: $_" }
        Log "=== PILOT FETCH COMPLETE ==="
        break
    }

    # --- Restart fetch if it died ---
    if (-not (Fetch-IsRunning)) {
        if ($stallSince -and (((Get-Date) - $stallSince).TotalMinutes -ge ($StallMinutes * 1.5))) {
            Log "Fetch not running + cache stalled — likely API daily limit. Sleeping 45 min then retry..."
            Start-Sleep -Seconds 2700
            $stallSince = $null
        }
        Log "Fetch process not running — restarting..."
        $fetchProc = Start-FetchProcess
    }

    # --- Periodic pipeline (assemble/filter/export) ---
    if (((Get-Date) - $lastPipeline).TotalSeconds -ge $PipelineIntervalSec) {
        Log "Scheduled pipeline pass..."
        & "$PSScriptRoot\run_pipeline.ps1" 2>&1 | ForEach-Object { Log "pipeline: $_" }
        $lastPipeline = Get-Date
    }

    Start-Sleep -Seconds $WatchIntervalSec
}

Log "=== Orchestrator finished ==="
Log "Run: powershell -ExecutionPolicy Bypass -File scripts\india_network\morning_report.ps1"

# Write quick status file
$done, $total = Get-PilotCompleteCount
@(
    "finished_at=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    "institutions_complete=$done/$total"
    "cache_files=$lastCacheCount"
) | Set-Content (Join-Path $LogDir "overnight_finished.txt")
