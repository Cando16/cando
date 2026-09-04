import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_inspect_endpoint():
    response = client.post("/api/text/inspect", json={"content": "This highlights the significance of robust process control.\u200B"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["artifacts"]) == 1
    assert data["artifacts"][0]["type"] == "invisible_unicode"
    
    # "robust process control" guards against importance puffery, but Faux Insight should still flag "This highlights the significance of"
    assert "Faux Insight" in data["patterns"]
    assert "Importance Puffery" not in data["patterns"]

def test_no_ai_slop_endpoint():
    response = client.post("/api/text/no-ai-slop", json={"content": "Furthermore, it is important to note that the sky is blue."})
    assert response.status_code == 200
    data = response.json()
    assert "Additionally, the sky is blue." == data["result"]

def test_cando_endpoint():
    # Because it's SSE, test client will consume the stream
    with client.stream("POST", "/api/text/cando", json={"content": "Furthermore, it is important to note that 520 °C is hot."}) as response:
        assert response.status_code == 200
        events = list(response.iter_lines())
        assert len(events) > 0
        last_event = events[-1]
        import json
        data = json.loads(last_event)
        assert data["step"] == "Done"
        assert "520 °C" in data["result"]["result"]
