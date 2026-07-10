@echo off
setlocal
pushd "%~dp0"
"C:\Users\User\.openclaw\tools\godot\Godot_v4.6.3-stable_win64_console.exe" --headless --path . --quit
popd
