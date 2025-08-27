import argparse, json, sys, os, glob
from tokra_shield.engine import analyze
from tokra_shield.ghost_loader import stats as rules_stats, available_langs
from tokra_shield.config import load_config
from tokra_shield.branding import print_banner

def _print(obj): print(json.dumps(obj, ensure_ascii=False, indent=2))

def _write(path:str, content:str, overwrite:bool=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and not overwrite: return
    with open(path, "w", encoding="utf-8") as f: f.write(content)

def main():
    p = argparse.ArgumentParser(prog="tokra-shield", description="Tokra Shield CLI")
    sub = p.add_subparsers(dest="cmd")

    hello = sub.add_parser("hello", help="show banner & quick info")

    run_p = sub.add_parser("run", help="launch REST API")
    run_p.add_argument("--host", default="0.0.0.0"); run_p.add_argument("--port", type=int, default=8099)
    run_p.add_argument("--workers", type=int, default=1); run_p.add_argument("--log-level", default="info")

    chk = sub.add_parser("check", help="single-shot analysis")
    chk.add_argument("text"); chk.add_argument("--lang", default="en"); chk.add_argument("--mode", default=None)
    chk.add_argument("--explain", action="store_true")

    lint = sub.add_parser("lint-rules", help="validate rules files")
    lint.add_argument("--dir", default=None); lint.add_argument("--lang", default="en")

    rstats = sub.add_parser("rules-stats", help="print rules stats")
    rstats.add_argument("--lang", default=None)

    init = sub.add_parser("init", help="scaffold overrides & sample config")
    init.add_argument("--dir", default="./tokra_overrides/ghost"); init.add_argument("--force", action="store_true")
    init.add_argument("--lang", nargs="+", default=["en"])

    doctor = sub.add_parser("doctor", help="environment & config report")

    args = p.parse_args()

    if args.cmd == "hello":
        print_banner(version="0.1.0", mode=load_config()["mode"])
        langs = available_langs()
        info = {l: rules_stats(l) for l in langs}
        _print({"langs":langs, "ruleset":info})
        print("\nTry: tokra-shield check \"click here\" --lang en")
        return

    if args.cmd == "run":
        from tokra_shield.api import app
        import uvicorn
        os.environ.setdefault("TOKRA_SHIELD_MAX_BODY","65536")
        uvicorn.run(app, host=args.host, port=args.port, workers=args.workers, log_level=args.log_level); return

    if args.cmd == "check":
        _print(analyze(args.text, args.lang, mode=args.mode, explain=args.explain)); return

    if args.cmd == "lint-rules":
        errs=[]; count=0; files=[]
        if args.dir: files = glob.glob(os.path.join(args.dir, "*.json"))
        for f in files:
            try:
                data=json.loads(open(f, "r", encoding="utf-8").read())
                for k,v in data.items():
                    if not isinstance(k,str): errs.append(f"{f}: key not str")
                    if not isinstance(v,dict): errs.append(f"{f}:{k}: value not object")
                    elif "type" not in v: errs.append(f"{f}:{k}: missing 'type'")
                count+=len(data)
            except Exception as e:
                errs.append(f"{f}: {e}")
        _print({"ok": len(errs)==0, "files": len(files), "rules": count, "errors": errs}); return

    if args.cmd == "rules-stats":
        langs = [args.lang] if args.lang else available_langs()
        _print({l: rules_stats(l) for l in langs}); return

    if args.cmd == "init":
        base = args.dir
        os.makedirs(base, exist_ok=True)
        for l in args.lang:
            _write(os.path.join(base, f"{l}.json"), '{\n  "your rule here": {"type":"spam","risk":10}\n}\n', overwrite=args.force)
        _print({"created": base, "files": sorted(os.listdir(base))})
        print("Set TOKRA_SHIELD_RULES_DIR=" + os.path.abspath(base))
        return

    if args.cmd == "doctor":
        cfg = load_config()
        try:
            import fastapi as _; api_available=True
        except Exception:
            api_available=False
        _print({
            "version":"0.1.0",
            "api_available": api_available,
            "mode": cfg["mode"],
            "thresholds": cfg["thresholds"],
            "cap": cfg["cap"],
            "allow_zero_sep_join": cfg["allow_zero_sep_join"],
            "langs": available_langs()
        }); return

    p.print_help(sys.stderr)
