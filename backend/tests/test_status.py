from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "provider_configured" in data
    assert "provider_reachable" in data
