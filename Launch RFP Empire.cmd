@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Install dependencies from this folder first: uv sync --locked --group dev
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m app %*
