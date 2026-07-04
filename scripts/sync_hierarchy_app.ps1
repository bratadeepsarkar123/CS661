# Sync dashboard India network JSON into hierarchy-app public/ and dist/.
# Run from repo root: .\scripts\sync_hierarchy_app.ps1
# Optional Vite rebuild requires hierarchy-app/package.json (not always present in repo).

$ErrorActionPreference = "Stop"
$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$Root = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$Src = Join-Path $Root "dashboard\data\india_network"
$DstPublic = Join-Path $Root "hierarchy-app\public\india_network"
$AppDir = Join-Path $Root "hierarchy-app"
$DstDist = Join-Path $AppDir "dist\india_network"

if (-not (Test-Path -LiteralPath $Src)) {
    Write-Error "Missing canonical data: $Src — run 09b_export_year_slices.py first."
}

New-Item -ItemType Directory -Force -Path $DstPublic | Out-Null
Copy-Item -Path (Join-Path $Src '*') -Destination $DstPublic -Recurse -Force
Write-Host "Synced -> $DstPublic"

New-Item -ItemType Directory -Force -Path $DstDist | Out-Null
Copy-Item -Path (Join-Path $Src '*') -Destination $DstDist -Recurse -Force
Write-Host "Synced -> $DstDist"

$DashFull = Join-Path $Src "2024_full.json"
$DistFull = Join-Path $DstDist "2024_full.json"
if ((Test-Path -LiteralPath $DashFull) -and (Test-Path -LiteralPath $DistFull)) {
    $h1 = (Get-FileHash -LiteralPath $DashFull -Algorithm MD5).Hash
    $h2 = (Get-FileHash -LiteralPath $DistFull -Algorithm MD5).Hash
    if ($h1 -eq $h2) {
        Write-Host "OK: dist 2024_full.json matches dashboard MD5"
    } else {
        Write-Warning "MD5 mismatch: dashboard vs dist 2024_full.json"
    }
}

$PkgJson = Join-Path $AppDir "package.json"
if (Test-Path -LiteralPath $PkgJson) {
    Push-Location -LiteralPath $AppDir
    try {
        Write-Host "npm run build..."
        npm run build
        if ($LASTEXITCODE -ne 0) { Write-Warning "npm run build failed (exit $LASTEXITCODE)" }
    } finally {
        Pop-Location
    }
} else {
    Write-Warning "hierarchy-app/package.json missing — skipped Vite build; dist JSON synced from dashboard."
}

Write-Host "Done. Serve hierarchy-app/dist for static preview."
