param(
  [string]$TaskName = 'OpenClaw Watchdog',
  [int]$IntervalSeconds = 300
)

$ErrorActionPreference = 'Stop'

$ScriptPath = Join-Path $PSScriptRoot 'start-openclaw-stack.ps1'
if (-not (Test-Path -LiteralPath $ScriptPath)) {
  throw "Missing watchdog script: $ScriptPath"
}

$PowerShell = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
$Args = "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`" -IntervalSeconds $IntervalSeconds"

$Action = New-ScheduledTaskAction -Execute $PowerShell -Argument $Args
$LogonTrigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$RepeatTrigger = New-ScheduledTaskTrigger `
  -Once `
  -At (Get-Date).Date `
  -RepetitionInterval (New-TimeSpan -Seconds $IntervalSeconds) `
  -RepetitionDuration (New-TimeSpan -Days 3650)

$Settings = New-ScheduledTaskSettingsSet `
  -AllowStartIfOnBatteries `
  -DontStopIfGoingOnBatteries `
  -StartWhenAvailable `
  -ExecutionTimeLimit (New-TimeSpan -Minutes 2) `
  -RestartCount 3 `
  -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask `
  -TaskName $TaskName `
  -Action $Action `
  -Trigger @($LogonTrigger, $RepeatTrigger) `
  -Settings $Settings `
  -Description 'Checks every few minutes and starts Ollama plus the OpenClaw gateway when needed.' `
  -Force | Out-Null

Start-ScheduledTask -TaskName $TaskName
Write-Host "Installed and started scheduled task: $TaskName"
