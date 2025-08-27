import os, json
from fastapi import FastAPI, Request, HTTPException, Query
from .engine import analyze
from .ghost_loader import stats as rules_stats
from .config import load_config

MAX_BODY = int(os.getenv("TOKRA_SHIELD_MAX_BODY", "65536"))
app = FastAPI(title="Tokra Shield API")

@app.get("/healthz")
async def healthz():
    return {"ok": True}

@app.get("/readyz")
async def readyz(lang: str = Query("en")):
    return {"ok": True, "rules": rules_stats(lang)}

@app.get("/version")
async def version():
    return {"version": "0.1.0"}

@app.get("/ruleset")
async def ruleset(lang: str = Query("en")):
    return rules_stats(lang)

@app.post("/analyze/")
async def analyze_endpoint(req: Request):
    body = await req.body()
    if len(body) > MAX_BODY:
        raise HTTPException(status_code=413, detail="Request body too large")
    try:
        data = json.loads(body.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    text = data.get("text","")
    lang = data.get("lang","en")
    mode = data.get("mode")  # optional override per-call
    explain = bool(data.get("explain", False))
    return analyze(text, lang, mode=mode, explain=explain)
