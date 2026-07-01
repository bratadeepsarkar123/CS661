# One pass: assemble cache -> filter edges -> feasibility -> export -> copy to dashboard
# Respects INDIA_ETL_MEMORY (default low). Set high for overnight: $env:INDIA_ETL_MEMORY='high'
$ErrorActionPreference = "Continue"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root

$Mem = if ($env:INDIA_ETL_MEMORY) { $env:INDIA_ETL_MEMORY } else { "low" }
$Heavy = $true
if ($Mem -eq "low" -and (Test-Path "data\processed\works_raw.parquet")) {
    $Heavy = $false
    Write-Host "Lightweight pipeline (INDIA_ETL_MEMORY=low, works_raw exists) — skipping 05b/06"
}

$LogDir = Join-Path $Root "data\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Log = Join-Path $LogDir "pipeline_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"

function Log($msg) {
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
    Write-Host $line
    Add-Content -Path $Log -Value $line
}

Log "=== Pipeline pass start ==="

Log "Step: 03a enrich institution master"
python scripts/india_network/03a_enrich_institution_master.py 2>&1 | Tee-Object -FilePath $Log -Append

Log "Step: 07 join Scimago quality"
python scripts/india_network/07_join_scimago_quality.py 2>&1 | Tee-Object -FilePath $Log -Append

Log "Step: 05b assemble works from cache (pilot top 30, memory=$Mem)"
if ($Heavy) {
    python scripts/india_network/05b_assemble_works_from_cache.py --pilot-top 30 --memory $Mem 2>&1 | Tee-Object -FilePath $Log -Append

    Log "Step: 06 build domestic edges (W1-W5 filters)"
    python scripts/india_network/06_build_domestic_edges.py 2>&1 | Tee-Object -FilePath $Log -Append
} else {
    Log "SKIP 05b/06 — use `$env:INDIA_ETL_MEMORY='high' overnight or delete works_raw to force rebuild"
}

Log "Step: 04 feasibility gate"
python scripts/india_network/04_feasibility_domestic_edges.py 2>&1 | Tee-Object -FilePath $Log -Append

Log "Step: 08 join NIRF funding (if CSV present)"
if (Test-Path "data\raw\nirf_research_projects.csv") {
    python scripts/india_network/01d_prepare_nirf_funding.py 2>&1 | Tee-Object -FilePath $Log -Append
    python scripts/india_network/08_join_nirf_funding.py 2>&1 | Tee-Object -FilePath $Log -Append
} else {
    Log "SKIP funding join — download free CSV from dataful.in/datasets/19311/"
}

Log "Step: 09b export year slices"
python scripts/india_network/09b_export_year_slices.py 2>&1 | Tee-Object -FilePath $Log -Append

Log "Step: 09 export JSON payloads"
python scripts/india_network/09_export_payloads.py --year 0 2>&1 | Tee-Object -FilePath $Log -Append

Log "Step: copy to dashboard/data/india_network"
$src = Join-Path $Root "public\india_network"
$dst = Join-Path $Root "dashboard\data\india_network"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Copy-Item (Join-Path $src "*") $dst -Force

Log "=== Pipeline pass complete -> $Log ==="
