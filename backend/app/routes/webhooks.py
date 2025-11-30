from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
import hmac
import hashlib
import json

from app.config import get_settings
from app.models.incident import Incident, SeverityLevel, IncidentStatus
from app.services.database import get_db
from app.services.incident_processor import IncidentProcessor
from app.services.redis_service import RedisService

router = APIRouter()
settings = get_settings()

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verify webhook signature for security"""
    expected_signature = hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

@router.post("/incident")
async def receive_incident_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Receive incident webhooks from monitoring tools
    Expected payload:
    {
        "title": "High Error Rate Detected",
        "service": "api-gateway",
        "error_type": "500_errors",
        "severity": "high",
        "metadata": {...},
        "stack_trace": "..."
    }
    """
    # Verify signature
    signature = request.headers.get("X-Webhook-Signature", "")
    body = await request.body()
    
    if not verify_webhook_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    payload = json.loads(body)
    
    # Create incident
    incident = Incident(
        title=payload.get("title", "Unknown Incident"),
        description=payload.get("description", ""),
        severity=SeverityLevel(payload.get("severity", "medium")),
        status=IncidentStatus.DETECTED,
        source="webhook",
        service_name=payload.get("service", "unknown"),
        error_type=payload.get("error_type", "unknown"),
        incident_metadata=payload.get("metadata", {}),  # CHANGED
        stack_trace=payload.get("stack_trace", "")
    )
    
    db.add(incident)
    db.commit()
    db.refresh(incident)
    
    # Publish to Redis for processing
    redis_service = RedisService()
    await redis_service.publish_incident(incident.id)
    
    # Process incident in background
    background_tasks.add_task(
        IncidentProcessor.process_incident,
        incident.id
    )
    
    return {
        "status": "received",
        "incident_id": incident.id,
        "message": "Incident processing initiated"
    }

@router.post("/logs")
async def receive_log_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """Handle log stream webhooks for error detection"""
    payload = await request.json()
    
    # Detect errors in logs (simplified)
    if "error" in payload.get("message", "").lower() or payload.get("level") == "error":
        # Trigger incident creation
        background_tasks.add_task(
            IncidentProcessor.create_from_logs,
            payload
        )
    
    return {"status": "processed"}

@router.post("/metrics")
async def receive_metrics_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    """Handle metrics webhooks for threshold breaches"""
    payload = await request.json()
    
    # Check if metrics breach thresholds
    metric_value = payload.get("value", 0)
    threshold = payload.get("threshold", 100)
    
    if metric_value > threshold:
        background_tasks.add_task(
            IncidentProcessor.create_from_metrics,
            payload
        )
    
    return {"status": "processed"}
