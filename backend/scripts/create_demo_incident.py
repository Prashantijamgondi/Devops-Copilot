import requests
import hmac
import hashlib
import json

BACKEND_URL = "http://localhost:8000"  # Change to your Render URL
WEBHOOK_SECRET = "your-webhook-secret"

def create_signature(payload: str) -> str:
    return "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

# Demo incident payload
incident_payload = {
    "title": "High Error Rate in Payment Service",
    "description": "500 errors increased by 300% in the last 5 minutes",
    "service": "payment-service",
    "error_type": "500_errors",
    "severity": "critical",
    "metadata": {
        "error_rate": "35%",
        "affected_users": 150,
        "region": "us-east-1"
    },
    "stack_trace": """
Traceback (most recent call last):
  File "/app/payment/processor.py", line 45, in process_payment
    result = payment_gateway.charge(amount)
  File "/app/lib/gateway.py", line 89, in charge
    raise GatewayTimeoutError("Payment gateway timeout")
GatewayTimeoutError: Payment gateway timeout
    """
}

payload_str = json.dumps(incident_payload)
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
print(f"Response: {response.json()}")
