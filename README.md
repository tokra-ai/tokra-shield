# TOKRA SHIELD

Lightweight content‑protection SDK and optional REST API.

## Install
```bash
# SDK only
pip install tokra-shield

# SDK + API (recommended)
pip install "tokra-shield[api]"
Windows (CLI best):
pipx install "tokra-shield[api]"
First Run
tokra-shield hello
tokra-shield check "click here to win free crypto!" --lang en
tokra-shield run   # REST :8099
Modes & Thresholds (ENV)
TOKRA_SHIELD_MODE = off|low|balanced|strict|paranoid
TOKRA_SHIELD_THRESH_FLAG / TOKRA_SHIELD_THRESH_BLOCK
TOKRA_SHIELD_WEIGHT_SPAM / _SCAM / _INJECTION
TOKRA_SHIELD_CAP
External Rules (no rebuild)
tokra-shield init --dir ./my_rules/ghost --lang en ar
export TOKRA_SHIELD_RULES_DIR=$PWD/my_rules/ghost
tokra-shield rules-stats
REST
curl -s -X POST :8099/analyze/ -H 'Content-Type: application/json' \
  -d '{"text":"ignore previous instructions","lang":"en","mode":"strict","explain":true}'
Compatibility
Response includes both modern fields and flagged_phrases for backward compatibility.

License: Apache‑2.0
