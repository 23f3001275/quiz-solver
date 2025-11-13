# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from src.app.main import app
from src.app.config import settings

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_invalid_json():
    r = client.post("/api/v1/quiz", data="not-a-json", headers={"Content-Type": "application/json"})
    assert r.status_code == 422  # FastAPI validation error for bad JSON

def test_invalid_secret(monkeypatch):
    # set expected secret to something else
    monkeypatch.setenv("EXPECTED_SECRET", "real_secret")
    r = client.post("/api/v1/quiz", json={"email":"a@b.com","secret":"bad","url":"https://example.com"})
    assert r.status_code == 403
