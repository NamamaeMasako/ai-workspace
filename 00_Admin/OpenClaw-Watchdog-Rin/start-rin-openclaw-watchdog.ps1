param(
  [switch]$Watch,
  [int]$IntervalSeconds = 300,
  [int]$OpenClawPort = 18789,
  [switch]$EnsureOllama,
  [int]$OllamaPort = 11434
)

$ErrorActionPreference = 'Stop'

$OpenClawHome = Join-Path $env:USERPROFILE '.openclaw'
$GatewayCmd = Join-Path $OpenClawHome 'gateway.cmd'
$LogDir = Join-Path $OpenClawHome 'logs'
$WatchLog = Join-Path $LogDir 'openclaw-watchdog-rin.log'
$OllamaExe = Join-Path $env:LOCALAPPDATA 'Programs\Ollama\ollama.exe'

function Write-WatchLog {
  param([string]$Message)

  if (-not (Test-Path -LiteralPath $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
  }

  $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  Add-Content -LiteralPath $WatchLog -Value "[$stamp] $Message"
}

function Test-LocalPort {
  param([int]$Port)

  try {
    $client = [System.Net.Sockets.TcpClient]::new()
    $asyncResult = $client.BeginConnect('127.0.0.1', $Port, $null, $null)
    $connected = $asyncResult.AsyncWaitHandle.WaitOne(1000, $false)

    if ($connected) {
      $client.EndConnect($asyncResult)
    }

    $client.Close()
    return $connected
  } catch {
    return $false
  }
}

function Ensure-OllamaService {
  if (-not $EnsureOllama) {
    return
  }

  $running = Get-Process -Name 'ollama' -ErrorAction SilentlyContinue |
    Where-Object { $_.Path -eq $OllamaExe -or $_.Path -like '*\Ollama\ollama.exe' }

  if ((Test-LocalPort -Port $OllamaPort) -or $running) {
    return
  }

  if (-not (Test-Path -LiteralPath $OllamaExe)) {
    Write-WatchLog "Ollama requested but executable not found: $OllamaExe"
    return
  }

  Start-Process -FilePath $OllamaExe -ArgumentList 'serve' -WindowStyle Hidden
  Write-WatchLog 'Started Ollama serve.'
}

function Ensure-OpenClawGateway {
  if (Test-LocalPort -Port $OpenClawPort) {
    return
  }

  if (-not (Test-Path -LiteralPath $GatewayCmd)) {
    Write-WatchLog "OpenClaw gateway command not found: $GatewayCmd"
    return
  }

  Start-Process -FilePath $GatewayCmd -WorkingDirectory $OpenClawHome -WindowStyle Hidden
  Write-WatchLog 'Started OpenClaw gateway.'
}

function Ensure-RinOpenClawStack {
  Ensure-OllamaService
  Start-Sleep -Seconds 2
  Ensure-OpenClawGateway
}

Write-WatchLog "Rin watchdog invoked. Watch=$Watch IntervalSeconds=$IntervalSeconds OpenClawPort=$OpenClawPort EnsureOllama=$EnsureOllama"

do {
  try {
    Ensure-RinOpenClawStack
  } catch {
    Write-WatchLog "Error: $($_.Exception.Message)"
  }

  if ($Watch) {
    Start-Sleep -Seconds $IntervalSeconds
  }
} while ($Watch)
