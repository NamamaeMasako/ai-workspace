# OpenClaw Watchdog - Rin

Windows logon watchdog for Rin's local OpenClaw device.

This version keeps the OpenClaw gateway available on:

- `127.0.0.1:18789`

Ollama is optional on this device. The default configuration does not try to start it because Rin's current Windows account does not have Ollama at the standard path:

```text
%LOCALAPPDATA%\Programs\Ollama\ollama.exe
```

## Install

Run from this folder:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-rin-openclaw-watchdog-task.ps1
```

To use a different interval:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-rin-openclaw-watchdog-task.ps1 -IntervalSeconds 180
```

To also watch Ollama later:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-rin-openclaw-watchdog-task.ps1 -EnsureOllama
```

## What It Does

- Checks whether `127.0.0.1:18789` is accepting TCP connections.
- Starts `%USERPROFILE%\.openclaw\gateway.cmd` when the gateway port is down.
- Runs as a Windows scheduled task named `OpenClaw Watchdog - Rin`.
- Sleeps between checks. The default interval is 300 seconds.

## Logs

Logs are written to:

```text
%USERPROFILE%\.openclaw\logs\openclaw-watchdog-rin.log
```

## Uninstall

```powershell
Unregister-ScheduledTask -TaskName "OpenClaw Watchdog - Rin" -Confirm:$false
```
