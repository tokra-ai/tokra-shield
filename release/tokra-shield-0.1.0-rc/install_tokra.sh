#!/usr/bin/env bash
set -euo pipefail
ENV="${ENV:-tokra_shield_env}"
clear || true
# Banner
if command -v pyfiglet >/dev/null 2>&1; then
  pyfiglet -w 100 "TOKRA SHIELD" || true
else
  printf '\n===== TOKRA SHIELD =====\n'
fi

python3 -m venv "$ENV"
# shellcheck disable=SC1090
source "$ENV/bin/activate"
python -m pip install -U pip >/dev/null

WHL=$(ls -1 dist/tokra_shield-*.whl 2>/dev/null | tail -n1 || true)

echo -n "Installing Tokra Shield "
spin='|/-\'; i=0
if [ -n "$WHL" ]; then
  (pip install "$WHL" fastapi==0.116.1 uvicorn==0.35.0 >/dev/null 2>&1) & PID=$!
else
  (pip install 'tokra-shield[api]' >/dev/null 2>&1) & PID=$!
fi
while kill -0 "$PID" 2>/dev/null; do i=$(( (i+1) %4 )); printf "\rInstalling Tokra Shield %s" "${spin:$i:1}"; sleep 0.1; done
wait "$PID" || { echo; echo "[ERROR] pip install failed"; exit 1; }
printf "\rInstalling Tokra Shield ✓         \n"

tokra-shield hello || true
echo
echo "[OK] To start API: source $ENV/bin/activate && tokra-shield run"
