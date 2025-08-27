from tokra_shield.engine import analyze
def test_zero_width():
    s = "free\u200bcrypto"
    out = analyze(s, "en")
    assert any(m["phrase"].lower()=="free crypto" for m in out["matches"])
def test_modes():
    out = analyze("click here and get free crypto", "en", mode="strict")
    assert out["action"] in ("flag","block")
