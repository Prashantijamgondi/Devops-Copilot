from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta

from app.services.database import get_db
from app.models.incident import Incident, IncidentAction, IncidentStatus, SeverityLevel
from pydantic import BaseModel

router = APIRouter()

# Response models
class IncidentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    severity: str
    status: str
    service_name: str
    error_type: str
    root_cause: Optional[str]
    resolution_steps: List[str]
    detected_at: str
    resolved_at: Optional[str]
    
    class Config:
        from_attributes = True

class IncidentActionResponse(BaseModel):
    id: int
    action_type: str
    description: str
    result: dict
    success: int
    created_at: str
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[IncidentResponse])
async def list_incidents(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    service: Optional[str] = None,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get list of incidents with filters"""
    query = db.query(Incident)
    
    if status:
        query = query.filter(Incident.status == IncidentStatus(status))
    if severity:
        query = query.filter(Incident.severity == SeverityLevel(severity))
    if service:
        query = query.filter(Incident.service_name == service)
    
    incidents = query.order_by(desc(Incident.detected_at)).offset(offset).limit(limit).all()
    
    return [IncidentResponse(
        id=i.id,
        title=i.title,
        description=i.description,
        severity=i.severity.value,
        status=i.status.value,
        service_name=i.service_name,
        error_type=i.error_type,
        root_cause=i.root_cause,
        resolution_steps=i.resolution_steps or [],
        detected_at=i.detected_at.isoformat(),
        resolved_at=i.resolved_at.isoformat() if i.resolved_at else None
    ) for i in incidents]

@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    """Get incident details"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return IncidentResponse(
        id=incident.id,
        title=incident.title,
        description=incident.description,
        severity=incident.severity.value,
        status=incident.status.value,
        service_name=incident.service_name,
        error_type=incident.error_type,
        root_cause=incident.root_cause,
        resolution_steps=incident.resolution_steps or [],
        detected_at=incident.detected_at.isoformat(),
        resolved_at=incident.resolved_at.isoformat() if incident.resolved_at else None
    )

@router.get("/{incident_id}/actions", response_model=List[IncidentActionResponse])
async def get_incident_actions(
    incident_id: int,
    db: Session = Depends(get_db)
):
    """Get all actions taken for an incident"""
    actions = db.query(IncidentAction).filter(
        IncidentAction.incident_id == incident_id
    ).all()
    
    return [IncidentActionResponse(
        id=a.id,
        action_type=a.action_type,
        description=a.description,
        result=a.result or {},
        success=a.success,
        created_at=a.created_at.isoformat()
    ) for a in actions]

@router.put("/{incident_id}/status")
async def update_incident_status(
    incident_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update incident status (called by Kestra workflows)"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    incident.status = IncidentStatus(status)
    
    if status == "resolved":
        incident.resolved_at = datetime.utcnow()
    
    db.commit()
    
    return {"status": "updated", "incident_id": incident_id}
