param(
  [string]$TaskName = 'OpenClaw Watchdog - Rin',
  [int]$IntervalSeconds = 300,
  [int]$OpenClawPort = 18789,
  [switch]$EnsureOllama,
  [int]$OllamaPort = 11434
)

$ErrorActionPreference = 'Stop'

$ScriptPath = Join-Path $PSScriptRoot 'start-rin-openclaw-watchdog.ps1'
if (-not (Test-Path -LiteralPath $ScriptPath)) {
  throw "Missing Rin watchdog script: $ScriptPath"
}

$PowerShell = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
$Arguments = @(
  '-NoProfile',
  '-ExecutionPolicy Bypass',
  '-File',
  "`"$ScriptPath`"",
  '-Watch',
  '-IntervalSeconds',
  $IntervalSeconds,
  '-OpenClawPort',
  $OpenClawPort
)

if ($EnsureOllama) {
  $Arguments += @('-EnsureOllama', '-OllamaPort', $OllamaPort)
}

$Action = New-ScheduledTaskAction -Execute $PowerShell -Argument ($Arguments -join ' ')
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$Settings = New-ScheduledTaskSettingsSet `
  -AllowStartIfOnBatteries `
  -DontStopIfGoingOnBatteries `
  -ExecutionTimeLimit (New-TimeSpan -Days 365) `
  -RestartCount 3 `
  -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask `
  -TaskName $TaskName `
  -Action $Action `
  -Trigger $Trigger `
  -Settings $Settings `
  -Description 'Rin device watchdog that keeps the local OpenClaw gateway available after Windows logon.' `
  -Force | Out-Null

Start-ScheduledTask -TaskName $TaskName
Write-Host "Installed and started scheduled task: $TaskName"
