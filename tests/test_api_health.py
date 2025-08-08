from fastapi.testclient import TestClient
from ai_sport_agent.api.v1 import app

def test_health_endpoint():
    client = TestClient(app)
    resp = client.get("/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
