import json, os
from importlib import resources as ir
from pathlib import Path
_CACHE={}
def _load_json(p:Path)->dict:
  try: return json.loads(p.read_text(encoding="utf-8"))
  except Exception: return {}
def load_ghost_data(lang:str="en")->dict:
  if lang in _CACHE: return _CACHE[lang]
  data={}
  try:
    p = ir.files("tokra_shield.ghost").joinpath(f"{lang}.json")
    data.update(json.loads(p.read_text(encoding="utf-8")))
  except Exception: pass
  for d in filter(None,[os.getenv("TOKRA_SHIELD_RULES_DIR"), "/etc/tokra_shield/ghost"]):
    f = Path(d)/f"{lang}.json"
    if f.is_file(): data.update(_load_json(f))
  _CACHE[lang]=data
  return data
def stats(lang:str="en")->dict:
  d = load_ghost_data(lang)
  cats={}
  for _,m in d.items():
    t=(m or {}).get("type","unknown")
    cats[t]=cats.get(t,0)+1
  return {"lang":lang,"count":len(d),"by_type":cats}
def available_langs()->list[str]:
  langs=set()
  # built-in
  try:
    for p in ir.files("tokra_shield.ghost").iterdir():
      name=getattr(p,"name",None)
      if name and name.endswith(".json"): langs.add(name[:-5])
  except Exception: pass
  # overrides
  for d in filter(None,[os.getenv("TOKRA_SHIELD_RULES_DIR"), "/etc/tokra_shield/ghost"]):
    pp=Path(d)
    if pp.is_dir():
      for f in pp.glob("*.json"): langs.add(f.stem)
  return sorted(langs or {"en"})
