# Snapshot checkpoint before overnight runs (restore = copy back from latest folder).
param([string]$Label = "manual")

$ErrorActionPreference = "Stop"
$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $Root

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$dest = Join-Path $Root "data\checkpoints\$ts`_$Label"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

$paths = @(
    "data\processed",
    "data\raw",
    "dashboard\data\india_network",
    "public\india_network"
)

foreach ($rel in $paths) {
    $src = Join-Path $Root $rel
    if (Test-Path $src) {
        $target = Join-Path $dest $rel
        New-Item -ItemType Directory -Force -Path (Split-Path $target -Parent) | Out-Null
        Copy-Item $src $target -Recurse -Force
    }
}

# Pointer to latest checkpoint
@{
    checkpoint = $dest
    created_at = (Get-Date).ToString("o")
    label = $Label
} | ConvertTo-Json | Set-Content (Join-Path $Root "data\checkpoints\LATEST.json") -Encoding UTF8

Write-Host "Checkpoint -> $dest"
