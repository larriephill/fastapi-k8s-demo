from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_root_has_service_name():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json().get("service") == "fastapi-k8s-demo"
