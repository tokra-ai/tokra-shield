from tokra_shield import analyze

def test_basic():
    res = analyze("Click here to get free crypto!", "en")
    assert {"click here", "free crypto"} <= set(res["flagged_phrases"])
    assert res["risk_score"] >= 30
