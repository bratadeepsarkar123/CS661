# Watchdog: restarts overnight_supervisor.py if it dies. Run alongside supervisor.
param([int]$MaxHours = 9)

$Root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$LogDir = Join-Path $Root "data\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Log = Join-Path $LogDir "watchdog.log"
$Deadline = (Get-Date).AddHours($MaxHours)

function WLog($m) {
    $l = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $m"
    Add-Content $Log $l
    Write-Host $l
}

function Supervisor-Running {
    Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -match "overnight_supervisor" } |
        Select-Object -First 1
}

WLog "Watchdog started (until $($Deadline.ToString('HH:mm')))"

while ((Get-Date) -lt $Deadline) {
    if (-not (Supervisor-Running)) {
        WLog "Supervisor not running - restarting..."
        Start-Process python -ArgumentList "scripts/india_network/overnight_supervisor.py --hours 8" `
            -WorkingDirectory $Root -WindowStyle Hidden
        Start-Sleep -Seconds 30
    }
    Start-Sleep -Seconds 120
}

WLog "Watchdog finished"

