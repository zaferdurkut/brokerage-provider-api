from starlette.testclient import TestClient

from main import app

client = TestClient(app)


def test_should_check_health():
    response = client.get("/api/healthcheck")
    assert response.status_code == 200
