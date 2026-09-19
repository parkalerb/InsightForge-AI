from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check_returns_200_and_valid_payload():
    """Verify that GET /health returns HTTP 200 and expected health status structure."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "app_name" in data
    assert "environment" in data
    assert data["app_name"] == "InsightForge AI"
