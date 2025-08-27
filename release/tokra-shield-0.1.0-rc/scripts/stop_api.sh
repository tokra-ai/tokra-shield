#!/usr/bin/env bash
set -euo pipefail
APP_DIR="${APP_DIR:-$HOME/tokra_shield_pkg}"
PORT="${PORT:-8099}"
cd "$APP_DIR"
if [ -f run/api.pid ]; then
  PID=$(cat run/api.pid) || true
  [ -n "${PID:-}" ] && kill -9 "$PID" || true
  rm -f run/api.pid
fi
PIDP=$(ss -ltnp | awk -v p=":$PORT" '$0 ~ p {print $NF}' | sed -E 's/.*pid=([0-9]+).*/\1/' | head -n1 || true)
[ -n "${PIDP:-}" ] && kill -9 "$PIDP" || true
echo "[STOPPED]"
