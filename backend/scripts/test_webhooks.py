"""Test webhook endpoints"""
import requests
import json
import hmac
import hashlib

BACKEND_URL = "http://localhost:8000"
WEBHOOK_SECRET = "your-webhook-secret-here"

def create_signature(payload: str) -> str:
    return "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

def test_incident_webhook():
    """Test incident creation via webhook"""
    payload = {
        "title": "Test Incident - API Latency Spike",
        "description": "P99 latency increased to 2.5s (threshold: 500ms)",
        "service": "checkout-service",
        "error_type": "latency_spike",
        "severity": "high",
        "metadata": {
            "p50_latency": "150ms",
            "p99_latency": "2500ms",
            "affected_endpoints": ["/api/checkout", "/api/payment"]
        },
        "stack_trace": "N/A - Performance degradation"
    }
    
    payload_str = json.dumps(payload)
    signature = create_signature(payload_str)
    
    response = requests.post(
        f"{BACKEND_URL}/api/v1/webhooks/incident",
        headers={
            "X-Webhook-Signature": signature,
            "Content-Type": "application/json"
        },
        data=payload_str
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_log_webhook():
    """Test log ingestion webhook"""
    payload = {
        "timestamp": "2025-11-29T02:00:00Z",
        "level": "error",
        "service": "auth-service",
        "message": "Failed to validate JWT token: signature verification failed",
        "trace_id": "abc123",
        "metadata": {
            "user_id": "user_789",
            "endpoint": "/api/auth/verify"
        }
    }
    
    response = requests.post(
        f"{BACKEND_URL}/api/v1/webhooks/logs",
        json=payload
    )
    
    print(f"Log webhook status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_metrics_webhook():
    """Test metrics threshold webhook"""
    payload = {
        "metric_name": "error_rate",
        "service": "payment-service",
        "value": 15.5,
        "threshold": 5.0,
        "unit": "percent",
        "timestamp": "2025-11-29T02:00:00Z"
    }
    
    response = requests.post(
        f"{BACKEND_URL}/api/v1/webhooks/metrics",
        json=payload
    )
    
    print(f"Metrics webhook status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("Testing incident webhook...")
    test_incident_webhook()
    
    print("\nTesting log webhook...")
    test_log_webhook()
    
    print("\nTesting metrics webhook...")
    test_metrics_webhook()
