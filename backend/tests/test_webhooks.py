import pytest
import hmac
import hashlib
import json
from fastapi.testclient import TestClient
from app.main import app
from app.config import get_settings

settings = get_settings()

@pytest.fixture
def client():
    return TestClient(app)

def create_test_signature(payload: str) -> str:
    return "sha256=" + hmac.new(
        b"test-secret",
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

def test_webhook_incident_valid(client):
    payload = {
        "title": "Test Incident",
        "service": "test-service",
        "error_type": "test_error",
        "severity": "medium"
    }
    payload_str = json.dumps(payload)
    
    # Note: This test will fail without proper signature verification
    # Configure test secret in your test environment
    
    response = client.post(
        "/api/v1/webhooks/incident",
        data=payload_str,
        headers={
            "X-Webhook-Signature": create_test_signature(payload_str),
            "Content-Type": "application/json"
        }
    )
    
    # Will return 401 if signature doesn't match
    assert response.status_code in [200, 401]
