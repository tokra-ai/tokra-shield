#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${APP_DIR:-$HOME/tokra_shield_pkg}"
PORT="${PORT:-8099}"
cd "$APP_DIR"
./scripts/stop_api.sh || true
rm -rf tokra_shield.egg-info build dist .venv_smoke
echo "[OK] Uninstalled runtime artifacts (kept sources)"
