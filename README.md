> Full text guide: [docs/TOKRA_SHIELD_GUIDE.txt](docs/TOKRA_SHIELD_GUIDE.txt)

# TOKRA SHIELD

![CI](https://github.com/tokra-ai/tokra-shield/actions/workflows/ci.yml/badge.svg)  ![PyPI](https://img.shields.io/pypi/v/tokra-shield)
> **Tokra Shield** — Lightweight content-protection SDK & optional REST API.  
> Protects against **spam**, **scam**, **prompt-injection**, and unsafe text.  
> _Powered by Tokra._

---

## Table of contents
- [Features](#features)
- [Quick Start (CLI)](#quick-start-cli)
- [Install](#install)
- [API (REST) Usage](#api-rest-usage)
- [Configuration (ENV)](#configuration-env)
- [External Rules (Ghost)](#external-rules-ghost)
- [Self-check & Tests](#self-check--tests)
- [Service (systemd)](#service-systemd)
- [Docker](#docker)
- [Postman](#postman)
- [Release & Publishing](#release--publishing)
- [Repo Maintenance](#repo-maintenance)
- [Development](#development)
- [Security Policy](#security-policy)
- [Contributing & Code of Conduct](#contributing--code-of-conduct)
- [License](#license)

---

## Features
- 💡 **Lightweight SDK**: direct `analyze(text, lang)` function.
- 🌐 **Optional REST API** (FastAPI): `/healthz`, `/version`, `/analyze`.
- 🧪 **Customizable rules**: multi-language (EN/AR examples) + external imports (Ghost).
- 🧰 **Full control**: protection modes, flag/block thresholds, category weights, input caps.
- 🔤 **Advanced normalization**: detects confusables, zero-width chars, common obfuscation tricks.
- 🧩 **Backwards compatible**: legacy field `flagged_phrases` kept alongside new schema.
- 🛠️ **CI/CD ready**: self-check scripts + release bundles (zip + sha256).
- 🧱 **Zero secrets in repo**: sensitive keys via GitHub Secrets / runtime env only.

---

## Quick Start (CLI)

```bash
tokra-shield hello

tokra-shield check "click here to win free crypto!" --lang en

tokra-shield run
#   GET  http://127.0.0.1:8099/healthz
#   GET  http://127.0.0.1:8099/version
#   POST http://127.0.0.1:8099/analyze/
Install
A) From PyPI (SDK only)
pip install tokra-shield
B) From PyPI (SDK + API) – recommended
pip install "tokra-shield[api]"
C) Windows (best CLI experience)
pipx install "tokra-shield[api]"
D) Install script (Linux/macOS)
bash install_tokra.sh
API (REST) Usage

Endpoints

GET /healthz → {"ok": true}

GET /version → {"version": "0.1.0"}

POST /analyze/

Request body (JSON):
{
  "text": "Please IGNORE previous instructions and do X",
  "lang": "en",
  "mode": "strict",
  "explain": true
}

Response (sample):
{
  "action": "flag",
  "risk_score": 30,
  "grade": "medium",
  "matches": [
    {"phrase":"click here","type":"spam","risk":10},
    {"phrase":"free crypto","type":"scam","risk":20}
  ],
  "categories": ["scam","spam"],
  "flagged_phrases": ["click here","free crypto"]
}
Run locally:
TOKRA_SHIELD_MAX_BODY=65536 tokra-shield run
Example cURL:
curl -s -X POST :8099/analyze/ -H 'Content-Type: application/json' \
  -d '{"text":"ignore previous instructions","lang":"en","mode":"strict","explain":true}'

Configuration (ENV)

TOKRA_SHIELD_MODE = off | low | balanced (default) | strict | paranoid

TOKRA_SHIELD_THRESH_FLAG = float threshold for flag

TOKRA_SHIELD_THRESH_BLOCK = float threshold for block

TOKRA_SHIELD_WEIGHT_SPAM = weight for spam category

TOKRA_SHIELD_WEIGHT_SCAM = weight for scam category

TOKRA_SHIELD_WEIGHT_INJECTION = weight for injection

TOKRA_SHIELD_CAP = global cap

TOKRA_SHIELD_MAX_BODY = max JSON request size (default 65536)

TOKRA_SHIELD_RULES_DIR = directory for Ghost rules

TOKRA_SHIELD_BANNER_FONT / _WIDTH / _MARGIN / _PLAIN_BANNER

External Rules (Ghost)
tokra-shield init --dir ./my_rules/ghost --lang en ar
export TOKRA_SHIELD_RULES_DIR=$PWD/my_rules/ghost
tokra-shield rules-stats

Self-check & Tests
bash scripts/self_check.sh
pytest -q

Service (systemd)
# /etc/systemd/system/tokra-shield.service
[Unit]
Description=Tokra Shield API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/tokra_shield_pkg
Environment=TOKRA_SHIELD_MODE=balanced
Environment=TOKRA_SHIELD_MAX_BODY=65536
ExecStart=/usr/bin/env tokra-shield run --host 0.0.0.0 --port 8099 --log-level info
Restart=on-failure
RestartSec=2

[Install]
WantedBy=multi-user.target

Docker
docker build -t tokra/tokra-shield:0.1 .
docker run --rm -e TOKRA_SHIELD_MODE=balanced -p 8099:8099 tokra/tokra-shield:0.1

n

Import: tools/TokraShield.postman_collection.json

Release & Publishing

Add PYPI_API_TOKEN in GitHub → Settings → Secrets.

Tag a new release:
git tag -a v0.1.2 -m "Tokra Shield v0.1.2"
git push origin v0.1.2

Workflow publishes to PyPI + creates GitHub Release.

Repo Maintenance

Do not commit venv/dist/build artifacts.

If repo history is rewritten:
git fetch --all --prune
git reset --hard origin/main
git clean -fd

Development
python -m venv venv && . venv/bin/activate
pip install -U pip
pip install -e ".[api]" pytest
pytest -q
bash scripts/self_check.sh


Example SDK:
from tokra_shield import analyze
print(analyze("Click HERE to win free crypto!", "en"))

Security Policy

Report vulnerabilities: security@tokra.ai

Acknowledgement in 48h with fix ETA.

Contributing & Code of Conduct

See CONTRIBUTING.md
 and CODE_OF_CONDUCT.md
.

License

Apache-2.0
