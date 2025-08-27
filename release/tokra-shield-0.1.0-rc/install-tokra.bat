@echo off
title TOKRA SHIELD Installer
echo.
echo ===== TOKRA SHIELD =====
set ENV=tokra_shield_env
py -m venv %ENV% 2>nul || python -m venv %ENV%
call %ENV%\Scripts\activate.bat
python -m pip install --upgrade pip >NUL
for %%f in (dist\tokra_shield-*.whl) do set WHL=%%f
if defined WHL (
  python -m pip install "%WHL%" fastapi==0.116.1 uvicorn==0.35.0
) else (
  python -m pip install "tokra-shield[api]"
)
tokra-shield hello
echo.
echo [OK] To start API: tokra-shield run
