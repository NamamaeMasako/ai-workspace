@echo off
setlocal
pushd "%~dp0"
echo Starting Godot from current folder.
echo If the game closes, copy/screenshot the log below.
echo.
"C:\Users\User\.openclaw\tools\godot\Godot_v4.6.3-stable_win64_console.exe" --path . --verbose
popd
pause
