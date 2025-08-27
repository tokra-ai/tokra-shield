#!/usr/bin/env bash
set -euo pipefail
ROOT="${ROOT:-$HOME/tokra_shield_pkg}"
cd "$ROOT"
VER=$(awk -F'"' '/^version/ {print $2}' pyproject.toml)
NAME="tokra-shield-${VER}-rc"
OUT="release/$NAME"

rm -rf release dist build *.egg-info
mkdir -p "$OUT" "$OUT/scripts" "$OUT/tools" "$OUT/docs"

python -m pip install -U build >/dev/null
python -m build

cp -a dist "$OUT/"
[ -f requirements-api.txt ] && cp -a requirements-api.txt "$OUT/" || true
[ -f run/.env.example ] && cp -a run/.env.example "$OUT/run.env.example" || true
cp -a scripts/start_api.sh scripts/stop_api.sh scripts/status_api.sh scripts/restart_api.sh scripts/self_check.sh "$OUT/scripts/"

[ -f tools/TokraShield.postman_collection.json ] && cp -a tools/TokraShield.postman_collection.json "$OUT/tools/" || true
[ -f install_tokra.sh ]  && cp -a install_tokra.sh  "$OUT/" || true
[ -f install-tokra.ps1 ] && cp -a install-tokra.ps1 "$OUT/" || true
[ -f install-tokra.bat ] && cp -a install-tokra.bat "$OUT/" || true

cat > "$OUT/docs/QUICKSTART.txt" <<'DOC'
Quick Start
-----------
Linux/macOS:
  bash install_tokra.sh
  source tokra_shield_env/bin/activate
  tokra-shield hello
  tokra-shield run   # REST on :8099

Windows:
  install-tokra.bat
  tokra-shield hello
  tokra-shield run
DOC

export NAME OUT
ZIP="release/${NAME}.zip"
python - <<'PY'
import os, zipfile
name = os.environ["NAME"]; out = os.environ["OUT"]
zip_path = f"release/{name}.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for dp, _, fns in os.walk(out):
        for fn in fns:
            full = os.path.join(dp, fn)
            arc = os.path.relpath(full, "release")
            zf.write(full, arc)
print(zip_path)
PY

# sha256 (fallback to Python if tool missing)
sha256sum "$ZIP" > "$ZIP.sha256" 2>/dev/null || python - <<'PY'
import hashlib, os
p = f"release/{os.environ['NAME']}.zip"
h = hashlib.sha256()
with open(p, "rb") as f:
    for chunk in iter(lambda: f.read(1<<20), b""): h.update(chunk)
open(p + ".sha256", "w").write(f"{h.hexdigest()}  {p}\n")
print(h.hexdigest(), p)
PY

echo "[OK] Bundle: $ZIP"
