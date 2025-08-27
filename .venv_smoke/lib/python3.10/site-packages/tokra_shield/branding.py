import os, sys, shutil
TITLE = "TOKRA SHIELD — Lightweight content‑protection SDK"
TEXT  = "TOKRA SHIELD"

def _term_width(default=110):
    try: return shutil.get_terminal_size((default, 20)).columns
    except Exception: return default

def _figlet(text, font):
    try:
        import pyfiglet
        return pyfiglet.figlet_format(text, font=font)
    except Exception:
        return text + "\n"

def _center(block, width):
    lines = block.rstrip("\n").splitlines()
    return "\n".join(line.center(width) for line in lines) + "\n"

def _frame(block, width, use_unicode=True):
    if os.getenv("TOKRA_SHIELD_BANNER_FRAME") != "1": return block
    top = ("┏" if use_unicode else "+") + ("━" if use_unicode else "-")*(width-2) + ("┓" if use_unicode else "+")
    bot = ("┗" if use_unicode else "+") + ("━" if use_unicode else "-")*(width-2) + ("┛" if use_unicode else "+")
    return f"{top}\n{block}{bot}\n"

def banner() -> str:
    plain  = os.getenv("TOKRA_SHIELD_PLAIN_BANNER") == "1"
    font   = os.getenv("TOKRA_SHIELD_BANNER_FONT", "big")         # default adopted
    width  = int(os.getenv("TOKRA_SHIELD_BANNER_WIDTH", "110"))   # default adopted
    margin = int(os.getenv("TOKRA_SHIELD_BANNER_MARGIN", "1"))    # default adopted
    body   = _figlet(TEXT, font=font) if not plain else TEXT + "\n"
    body   = _center(body, width)
    if margin > 0: body = ("\n"*margin) + body + ("\n"*margin)
    body   = _frame(body, width, use_unicode=not plain)
    return body + TITLE.center(width)

def one_liner(version: str, mode: str) -> str:
    w = int(os.getenv("TOKRA_SHIELD_BANNER_WIDTH", "110"))
    return ("TOKRA SHIELD " + str(version) + " • mode=" + str(mode)).center(w)

def print_banner(version: str | None = None, mode: str | None = None):
    print(banner())
    if version or mode: print(one_liner(version or "", mode or ""))
