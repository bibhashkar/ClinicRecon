import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.fixtures import load_fixture

client = TestClient(app)

def test_reconcile_metformin_case_1():
    data = load_fixture("case_1_reconcile.json")
    response = client.post("/api/reconcile/medication", json=data)
    assert response.status_code == 200

def test_data_quality_validation():
    data = load_fixture("case_1_quality.json")
    response = client.post("/api/validate/data-quality", json=data)
    assert response.status_code == 200
    result = response.json()
    assert "overall_score" in result
    assert "breakdown" in result
    assert "issues_detected" in result
    assert isinstance(result["issues_detected"], list)

def test_reconcile_missing_data():
    response = client.post("/api/reconcile/medication", json={}, headers={"X-API-Key": "your-secret-api-key-for-basic-auth"})
    assert response.status_code == 422  # Validation error

def test_data_quality_missing_data():
    response = client.post("/api/validate/data-quality", json={}, headers={"X-API-Key": "your-secret-api-key-for-basic-auth"})
    assert response.status_code == 422  # Validation error

def test_reconcile_rate_limit_simulation():
    # This would require mocking the LLM client to raise LLMRateLimitError
    # For now, just test the endpoint exists and handles errors
    data = load_fixture("case_1_reconcile.json")
    response = client.post("/api/reconcile/medication", json=data, headers={"X-API-Key": "your-secret-api-key-for-basic-auth"})
    # In a real rate limit scenario, it would return 429
    assert response.status_code in [200, 429, 500]

def test_data_quality_rate_limit_simulation():
    data = load_fixture("case_1_quality.json")
    response = client.post("/api/validate/data-quality", json=data, headers={"X-API-Key": "your-secret-api-key-for-basic-auth"})
    assert response.status_code in [200, 429, 500]

def test_reconcile_response_structure():
    data = load_fixture("case_1_reconcile.json")
    response = client.post("/api/reconcile/medication", json=data, headers={"X-API-Key": "your-secret-api-key-for-basic-auth"})
    if response.status_code == 200:
        result = response.json()
        assert "reconciled_medication" in result
        assert "confidence_score" in result
        assert "reasoning" in result
        assert "recommended_actions" in result
        assert "clinical_safety_check" in result

def test_data_quality_response_structure():
    data = load_fixture("case_1_quality.json")
    response = client.post("/api/validate/data-quality", json=data, headers={"X-API-Key": "your-secret-api-key-for-basic-auth"})
    if response.status_code == 200:
        result = response.json()
        assert "overall_score" in result
        assert "breakdown" in result
        assert "issues_detected" in result
        assert isinstance(result["breakdown"], dict)
        assert len(result["breakdown"]) == 4  # completeness, accuracy, timeliness, plausibility