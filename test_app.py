from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_format():
    response = client.get("/format", params={"text": "hi"})
    assert response.status_code == 200
    assert response.json() == {"result": "<b><i><u>hi</u></i></b>"}


def test_format_missing_text():
    response = client.get("/format")
    assert response.status_code == 422


def test_format_empty_text():
    response = client.get("/format", params={"text": ""})
    assert response.status_code == 422


def test_format_text_too_long():
    response = client.get("/format", params={"text": "a" * 201})
    assert response.status_code == 422
