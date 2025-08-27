import os, json
DEFAULT = {
  "mode": "balanced",
  "thresholds": {"allow": 0, "flag": 30, "block": 60},
  "weights": {"spam": 10, "scam": 20, "injection": 30, "unknown": 5},
  "cap": 100,
  "allow_zero_sep_join": True
}
def _getenv(name, default=None, cast=None):
  v = os.getenv(name); 
  if v is None: return default
  try:
    return cast(v) if cast else v
  except Exception:
    return default
def load_config() -> dict:
  cfg = dict(DEFAULT)
  m = _getenv("TOKRA_SHIELD_MODE", cfg["mode"])
  if m in ("off","low","balanced","strict","paranoid"):
    cfg["mode"] = m
    if m=="off":      cfg["thresholds"]={"allow":0,"flag":999,"block":999}
    elif m=="low":    cfg["thresholds"]={"allow":0,"flag":20,"block":999}
    elif m=="balanced": cfg["thresholds"]={"allow":0,"flag":30,"block":60}
    elif m=="strict": cfg["thresholds"]={"allow":0,"flag":20,"block":40}
    elif m=="paranoid":cfg["thresholds"]={"allow":0,"flag":10,"block":20}
  allow = _getenv("TOKRA_SHIELD_THRESH_ALLOW", None, int)
  flag  = _getenv("TOKRA_SHIELD_THRESH_FLAG",  None, int)
  block = _getenv("TOKRA_SHIELD_THRESH_BLOCK", None, int)
  if flag is not None or block is not None or allow is not None:
    cfg["thresholds"] = {
      "allow": allow if allow is not None else cfg["thresholds"]["allow"],
      "flag":  flag  if flag  is not None else cfg["thresholds"]["flag"],
      "block": block if block is not None else cfg["thresholds"]["block"],
    }
  for k in list(cfg["weights"].keys()):
    env = _getenv(f"TOKRA_SHIELD_WEIGHT_{k.upper()}", None, int)
    if env is not None: cfg["weights"][k]=env
  cfg["cap"] = _getenv("TOKRA_SHIELD_CAP", cfg["cap"], int)
  cfg["allow_zero_sep_join"] = bool(int(_getenv("TOKRA_SHIELD_ALLOW_ZERO_SEP_JOIN", "1")))
  return cfg
def decide_action(score:int, thresholds:dict)->tuple[str,str]:
  if score >= thresholds["block"]: return "block","high" if score<90 else "critical"
  if score >= thresholds["flag"]:  return "flag","medium"
  return "allow","low"
