from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from app.services.database import get_db
from app.models.incident import Incident, SeverityLevel, IncidentStatus

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats(
    db: Session = Depends(get_db)
):
    """Get dashboard statistics"""
    
    # Total incidents
    total_incidents = db.query(func.count(Incident.id)).scalar()
    
    # Active incidents
    active_incidents = db.query(func.count(Incident.id)).filter(
        Incident.status.in_([IncidentStatus.DETECTED, IncidentStatus.ANALYZING, IncidentStatus.RESOLVING])
    ).scalar()
    
    # Resolved today
    today = datetime.utcnow().date()
    resolved_today = db.query(func.count(Incident.id)).filter(
        Incident.status == IncidentStatus.RESOLVED,
        func.date(Incident.resolved_at) == today
    ).scalar()
    
    # Average resolution time (in minutes)
    resolved_incidents = db.query(Incident).filter(
        Incident.status == IncidentStatus.RESOLVED,
        Incident.resolved_at.isnot(None)
    ).all()
    
    if resolved_incidents:
        resolution_times = [
            (i.resolved_at - i.detected_at).total_seconds() / 60
            for i in resolved_incidents
        ]
        avg_resolution_time = sum(resolution_times) / len(resolution_times)
    else:
        avg_resolution_time = 0
    
    # Incidents by severity
    severity_counts = db.query(
        Incident.severity,
        func.count(Incident.id)
    ).group_by(Incident.severity).all()
    
    # Incidents by service (top 10)
    service_counts = db.query(
        Incident.service_name,
        func.count(Incident.id)
    ).group_by(Incident.service_name).order_by(
        desc(func.count(Incident.id))
    ).limit(10).all()
    
    # Incident trend (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    daily_counts = db.query(
        func.date(Incident.detected_at).label('date'),
        func.count(Incident.id).label('count')
    ).filter(
        Incident.detected_at >= seven_days_ago
    ).group_by(func.date(Incident.detected_at)).all()
    
    return {
        "total_incidents": total_incidents,
        "active_incidents": active_incidents,
        "resolved_today": resolved_today,
        "avg_resolution_time_minutes": round(avg_resolution_time, 2),
        "severity_distribution": {
            str(severity): count for severity, count in severity_counts
        },
        "top_services": [
            {"service": service, "count": count}
            for service, count in service_counts
        ],
        "daily_trend": [
            {"date": str(date), "count": count}
            for date, count in daily_counts
        ]
    }

@router.get("/mttr")
async def get_mttr(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Calculate Mean Time To Resolution"""
    
    since = datetime.utcnow() - timedelta(days=days)
    
    incidents = db.query(Incident).filter(
        Incident.status == IncidentStatus.RESOLVED,
        Incident.detected_at >= since,
        Incident.resolved_at.isnot(None)
    ).all()
    
    if not incidents:
        return {"mttr_minutes": 0, "sample_size": 0}
    
    resolution_times = [
        (i.resolved_at - i.detected_at).total_seconds() / 60
        for i in incidents
    ]
    
    mttr = sum(resolution_times) / len(resolution_times)
    
    return {
        "mttr_minutes": round(mttr, 2),
        "sample_size": len(incidents),
        "period_days": days
    }
