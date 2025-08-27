#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/tokra_shield_pkg}"
PORT="${PORT:-8099}"
HOST="${HOST:-0.0.0.0}"
WORKERS="${WORKERS:-1}"

cd "$APP_DIR"
. venv/bin/activate

# حمل المتغيرات إن وُجدت
[ -f run/env.sh ] && . run/env.sh

# تأكد من وجود الحزمة وملحقات API
python - <<'PY' >/dev/null 2>&1 || python -m pip install -e .[api] >/dev/null
import importlib; importlib.import_module('tokra_shield')
PY

mkdir -p run

# أغلق أي عملية قائمة على المنفذ
PID=$(ss -ltnp | awk -v p=":$PORT" '$0 ~ p {print $NF}' | sed -E 's/.*pid=([0-9]+).*/\1/' | head -n1 || true)
[ -n "${PID:-}" ] && kill -9 "$PID" || true

# شغّل (tokra-shield ثم fallback إلى python -m) مع لوق
nohup sh -lc '
  tokra-shield run --host "'"$HOST"'" --port "'"$PORT"'" --workers "'"$WORKERS"'" --log-level info \
  || python -m tokra_shield.cli run --host "'"$HOST"'" --port "'"$PORT"'" --workers "'"$WORKERS"'" --log-level info
' > run/api.log 2>&1 &

echo $! > run/api.pid

# انتظر الصحة
for i in $(seq 1 40); do
  if curl -fsS "http://127.0.0.1:$PORT/healthz" >/dev/null; then
    echo "[OK] API on http://127.0.0.1:$PORT"
    exit 0
  fi
  sleep 0.25
done
echo "[FAIL] API not responding"; tail -n 120 run/api.log; exit 1
