@echo off
setlocal
cd /d "%~dp0" || exit /b 1
if not exist ".bootstrap\uv.exe" (
  echo First launch: installing uv 0.11.6 from Astral into this folder. No administrator access is needed.
  set "UV_INSTALL_DIR=%CD%\.bootstrap"
  set "UV_NO_MODIFY_PATH=1"
  powershell.exe -NoProfile -Command "$ErrorActionPreference='Stop'; try { Invoke-RestMethod 'https://astral.sh/uv/0.11.6/install.ps1' | Invoke-Expression } catch { Write-Error $_; exit 1 }"
  if errorlevel 1 goto failed
)
echo Preparing RFP Locator. Python 3.12 and locked dependencies download automatically on first launch.
set "UV_LINK_MODE=copy"
".bootstrap\uv.exe" sync --locked --no-dev
if errorlevel 1 goto failed
echo Opening the local app. Keep this terminal open; stop the service from Settings when finished.
".venv\Scripts\python.exe" -m app %*
if errorlevel 1 goto failed
exit /b 0
:failed
echo Setup could not finish. Check your internet connection and folder permissions, then try again. See README.md for help.
if not defined CI pause
exit /b 1
