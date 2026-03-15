import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.fixtures import load_fixture

client = TestClient(app)

def test_reconcile_metformin_case_1():
    data = load_fixture("case_1_reconcile.json")
    response = client.post("/api/reconcile/medication", json=data, headers={"X-API-Key": "your-secret-api-key-for-basic-auth"})
    assert response.status_code == 200
    assert response.json()["confidence_score"] > 0.8
    assert "eGFR" in response.json()["reasoning"]  # clinical context used

def test_data_quality_validation():
    data = load_fixture("case_1_quality.json")
    response = client.post("/api/validate/data-quality", json=data, headers={"X-API-Key": "your-secret-api-key-for-basic-auth"})
    assert response.status_code == 200
    result = response.json()
    assert "overall_score" in result
    assert "breakdown" in result
    assert "issues_detected" in result
    assert isinstance(result["issues_detected"], list)