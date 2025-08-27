#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${APP_DIR:-$HOME/tokra_shield_pkg}"
cd "$APP_DIR"
./scripts/stop_api.sh || true
./scripts/start_api.sh
