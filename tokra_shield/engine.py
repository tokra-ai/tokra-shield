from .ghost_loader import load_ghost_data
from .normalizer import normalize, strip_spaces
from .config import load_config, decide_action
def analyze(text:str, lang:str="en", *, mode:str|None=None, explain:bool=False)->dict:
    cfg = load_config()
    if mode: cfg["mode"] = mode
    thresholds = cfg["thresholds"]; weights = cfg["weights"]; cap = cfg["cap"]
    allow_zero_sep_join = cfg["allow_zero_sep_join"]
    ghost = load_ghost_data(lang) or {}
    txt_norm = normalize(text, allow_zero_sep=True)
    txt_nospace = strip_spaces(txt_norm)
    matches=[]; cats=set(); score=0
    for phrase, meta in ghost.items():
        meta = meta or {}
        ph_norm = normalize(phrase, allow_zero_sep=True)
        if not ph_norm: continue
        hit = (ph_norm in txt_norm) or (allow_zero_sep_join and strip_spaces(ph_norm) in txt_nospace)
        if hit:
            t = meta.get("type","unknown")
            r = meta.get("risk", weights.get(t,5))
            matches.append({"phrase":phrase,"type":t,"risk":r})
            cats.add(t); score += r
    if score>cap: score=cap
    action, grade = decide_action(score, thresholds)
    out = {"action":action,"risk_score":score,"grade":grade,"matches":matches,"categories":sorted(cats)}
    out["flagged_phrases"] = [m["phrase"] for m in matches]  # back-compat
    if explain: out["debug"]={"mode":cfg["mode"],"thresholds":thresholds,"cap":cap}
    return out
