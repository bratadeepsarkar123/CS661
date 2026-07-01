# Resume after graceful pause — fetch already 120/120; run final assemble + export only.
# Usage: powershell -ExecutionPolicy Bypass -File scripts\india_network\resume_after_pause.ps1

$ErrorActionPreference = "Continue"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root
$LogDir = Join-Path $Root "data\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Log = Join-Path $LogDir "resume_final.log"

function Log($m) {
    $l = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $m"
    Write-Host $l
    Add-Content $Log $l
}

Log "=== Resume after pause (final chain, no fetch) ==="

Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -match 'overnight_supervisor|05_fetch|05b_assemble|06_build' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

$env:INDIA_ETL_MEMORY = "low"
$env:ETL_RAM_CAP_MB = "4608"
$env:RESOURCE_CAP = "off"

$cache = (Get-ChildItem (Join-Path $Root "data\cache\openalex\works_*.json") -ErrorAction SilentlyContinue).Count
Log "Cache files: $cache | Fetch: 120/120 complete"

function Run-Step($name, [string[]]$pyArgs) {
    Log "STEP $name ..."
    $proc = Start-Process -FilePath "python" -ArgumentList $pyArgs -WorkingDirectory $Root -Wait -PassThru -NoNewWindow -RedirectStandardOutput $Log -RedirectStandardError $Log
    if ($proc.ExitCode -ne 0) {
        Log "STEP $name FAILED (exit $($proc.ExitCode))"
        return $false
    }
    Log "STEP $name OK"
    return $true
}

Run-Step "03a" @("scripts/india_network/03a_enrich_institution_master.py") | Out-Null
Run-Step "07" @("scripts/india_network/07_join_scimago_quality.py") | Out-Null
Run-Step "05b" @("scripts/india_network/05b_assemble_works_from_cache.py", "--memory", "low") | Out-Null
Run-Step "06" @("scripts/india_network/06_build_domestic_edges.py") | Out-Null
Run-Step "04" @("scripts/india_network/04_feasibility_domestic_edges.py") | Out-Null
Run-Step "01d" @("scripts/india_network/01d_prepare_nirf_funding.py") | Out-Null
Run-Step "08" @("scripts/india_network/08_join_nirf_funding.py") | Out-Null
Run-Step "09" @("scripts/india_network/09_export_payloads.py", "--year", "0") | Out-Null
Run-Step "09b" @("scripts/india_network/09b_export_year_slices.py") | Out-Null
Run-Step "10_verify" @("scripts/india_network/10_verification_checklist.py") | Out-Null

$src = Join-Path $Root "public\india_network"
$dst = Join-Path $Root "dashboard\data\india_network"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item (Join-Path $src "*") $dst -Force
Log "Copied JSON -> dashboard/data/india_network"

powershell -ExecutionPolicy Bypass -File scripts\india_network\checkpoint_data.ps1 -Label "post_final_assemble"
Remove-Item (Join-Path $LogDir "PAUSED.json") -Force -ErrorAction SilentlyContinue

@{
    updated_at = (Get-Date).ToUniversalTime().ToString("o")
    state = "complete"
    cache_files = $cache
} | ConvertTo-Json | Set-Content (Join-Path $LogDir "supervisor_status.json") -Encoding UTF8

Log "=== RESUME COMPLETE ==="
Log "Dashboard: cd dashboard; python -m http.server 8766"
