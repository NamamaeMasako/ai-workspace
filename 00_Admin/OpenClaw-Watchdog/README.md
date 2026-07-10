# OpenClaw Watchdog

Windows logon watchdog for local OpenClaw setups.

It keeps these local services available:

- Ollama on `127.0.0.1:11434`
- OpenClaw gateway on `127.0.0.1:18789`

The scheduled task runs a short check at logon and then repeats every 300 seconds by default. It does not keep a long-running PowerShell process awake in the background.

## Install

Open PowerShell and run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-openclaw-watchdog-task.ps1
```

To use a different interval:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-openclaw-watchdog-task.ps1 -IntervalSeconds 300
```

The task is named `OpenClaw Watchdog`.

## Requirements

- OpenClaw home: `%USERPROFILE%\.openclaw`
- OpenClaw gateway launcher: `%USERPROFILE%\.openclaw\gateway.cmd`
- Ollama executable: `%LOCALAPPDATA%\Programs\Ollama\ollama.exe`

If another device uses different paths or ports, edit `start-openclaw-stack.ps1`.

## Logs

Logs are written to:

```text
%USERPROFILE%\.openclaw\logs\openclaw-watchdog.log
```

## Uninstall

```powershell
Unregister-ScheduledTask -TaskName "OpenClaw Watchdog" -Confirm:$false
```
