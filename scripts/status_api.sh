#!/usr/bin/env bash
set -euo pipefail
PORT="${PORT:-8099}"
echo "== LISTENERS :$PORT =="
ss -ltnp | grep ":$PORT" || echo "no listener"
echo "== LOG TAIL =="
tail -n 40 run/api.log 2>/dev/null || echo "no log"
