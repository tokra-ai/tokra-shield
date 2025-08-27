import os
from fastapi.testclient import TestClient
def test_health_and_version():
    os.environ["TOKRA_SHIELD_MAX_BODY"] = "65536"
    from importlib import reload
    import tokra_shield.api as api
    reload(api)
    c = TestClient(api.app)
    r = c.get("/healthz"); assert r.status_code == 200 and r.json().get("ok") is True
    r = c.get("/version"); assert r.status_code == 200 and "version" in r.json()
def test_analyze_small_request():
    from fastapi.testclient import TestClient
    from importlib import reload
    import tokra_shield.api as api
    reload(api)
    c = TestClient(api.app)
    r = c.post("/analyze/", json={"text":"click here to get free crypto!","lang":"en"})
    assert r.status_code == 200
    j = r.json()
    assert "free crypto" in j["flagged_phrases"]
def test_body_too_large():
    os.environ["TOKRA_SHIELD_MAX_BODY"] = "128"
    from importlib import reload
    import tokra_shield.api as api
    reload(api)
    from fastapi.testclient import TestClient
    c = TestClient(api.app)
    r = c.post("/analyze/", json={"text": "x"*1000, "lang": "en"})
    assert r.status_code == 413
