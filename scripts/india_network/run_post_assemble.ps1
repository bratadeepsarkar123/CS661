# Run after 05b completes: edges, export, verify, dashboard copy.
$ErrorActionPreference = "Continue"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root
$Log = Join-Path $Root "data\logs\resume_post_05b.log"

function Log($m) {
    $l = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $m"
    Write-Host $l
    Add-Content $Log $l
}

Log "=== Post-05b pipeline ==="
$steps = @(
    @("06", "scripts/india_network/06_build_domestic_edges.py"),
    @("04", "scripts/india_network/04_feasibility_domestic_edges.py"),
    @("01d", "scripts/india_network/01d_prepare_nirf_funding.py"),
    @("08", "scripts/india_network/08_join_nirf_funding.py"),
    @("09", "scripts/india_network/09_export_payloads.py", "--year", "0"),
    @("09b", "scripts/india_network/09b_export_year_slices.py"),
    @("10_verify", "scripts/india_network/10_verification_checklist.py")
)
foreach ($s in $steps) {
    $name = $s[0]
    $args = $s[1..($s.Length - 1)]
    Log "STEP $name ..."
    $p = Start-Process python -ArgumentList $args -WorkingDirectory $Root -Wait -PassThru -NoNewWindow
    if ($p.ExitCode -ne 0) { Log "STEP $name FAILED"; exit 1 }
    Log "STEP $name OK"
}
Copy-Item (Join-Path $Root "public\india_network\*") (Join-Path $Root "dashboard\data\india_network") -Force
Log "Dashboard updated"
powershell -ExecutionPolicy Bypass -File scripts\india_network\checkpoint_data.ps1 -Label "full_pipeline_complete"
Remove-Item (Join-Path $Root "data\logs\PAUSED.json") -Force -ErrorAction SilentlyContinue
Log "=== ALL DONE ==="
