from fastapi.testclient import TestClient

from src.main import app

# No `with` block: the startup event (database seeding) is intentionally not run,
# so these tests need no PostgreSQL instance.
client = TestClient(app)


def test_root_returns_metadata():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["docs"] == "/docs"
    assert "version" in body


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
