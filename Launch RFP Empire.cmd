@echo off
setlocal
cd /d "%~dp0" || exit /b 1
set "RFP_POWERSHELL=powershell.exe"
where pwsh.exe >nul 2>&1 && set "RFP_POWERSHELL=pwsh.exe"
if not exist ".bootstrap\uv.exe" (
  echo First launch: installing uv 0.11.6 from Astral into this folder. No administrator access is needed.
  "%RFP_POWERSHELL%" -NoProfile -Command "$ErrorActionPreference='Stop'; try { if (-not [Environment]::Is64BitOperatingSystem) { throw 'This preview requires 64-bit Windows.' }; New-Item -ItemType Directory -Force '.bootstrap' | Out-Null; $zip=Join-Path $PWD '.bootstrap\uv.zip'; Invoke-WebRequest -UseBasicParsing 'https://github.com/astral-sh/uv/releases/download/0.11.6/uv-x86_64-pc-windows-msvc.zip' -OutFile $zip; if ((Get-FileHash $zip -Algorithm SHA256).Hash -ne '99aa60edd017a256dbf378f372d1cff3292dbc6696e0ea01716d9158d773ab77') { throw 'uv download checksum mismatch. Please retry.' }; Expand-Archive -Force -Path $zip -DestinationPath '.bootstrap'; Remove-Item $zip } catch { Write-Error $_; exit 1 }"
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
