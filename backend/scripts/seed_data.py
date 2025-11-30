"""Seed database with sample incidents for demo"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.models.incident import Incident, SeverityLevel, IncidentStatus
from app.services.database import SessionLocal
from datetime import datetime, timedelta
import random

def seed_incidents():
    db = SessionLocal()
    
    sample_incidents = [
        {
            "title": "Database Connection Pool Exhausted",
            "description": "PostgreSQL connection pool reached maximum capacity",
            "service_name": "user-service",
            "error_type": "database_connection",
            "severity": SeverityLevel.CRITICAL,
            "status": IncidentStatus.RESOLVED,
            "root_cause": "Inefficient query causing connection leak"
        },
        {
            "title": "API Gateway Timeout",
            "description": "Gateway returning 504 errors for 15% of requests",
            "service_name": "api-gateway",
            "error_type": "timeout",
            "severity": SeverityLevel.HIGH,
            "status": IncidentStatus.RESOLVED,
            "root_cause": "Downstream service response time increased"
        },
        {
            "title": "Memory Usage Spike",
            "description": "Memory consumption at 95% on payment-service pods",
            "service_name": "payment-service",
            "error_type": "memory_leak",
            "severity": SeverityLevel.HIGH,
            "status": IncidentStatus.RESOLVED,
            "root_cause": "Memory leak in session handling"
        },
        {
            "title": "Redis Connection Errors",
            "description": "Intermittent Redis connection failures",
            "service_name": "cache-service",
            "error_type": "connection_error",
            "severity": SeverityLevel.MEDIUM,
            "status": IncidentStatus.RESOLVED,
            "root_cause": "Network partition between cache and app servers"
        },
        {
            "title": "High CPU Usage",
            "description": "CPU usage consistently above 80%",
            "service_name": "analytics-service",
            "error_type": "resource_exhaustion",
            "severity": SeverityLevel.MEDIUM,
            "status": IncidentStatus.ANALYZING,
            "root_cause": None
        },
        {
            "title": "Webhook Delivery Failures",
            "description": "Webhook POST requests failing with 500 errors",
            "service_name": "notification-service",
            "error_type": "webhook_failure",
            "severity": SeverityLevel.LOW,
            "status": IncidentStatus.DETECTED,
            "root_cause": None
        }
    ]
    
    for i, incident_data in enumerate(sample_incidents):
        detected_time = datetime.utcnow() - timedelta(hours=random.randint(1, 48))
        
        # Around line 80-90
        incident = Incident(
            **incident_data,
            detected_at=detected_time,
            resolved_at=detected_time + timedelta(minutes=random.randint(15, 120)) 
                    if incident_data["status"] == IncidentStatus.RESOLVED else None,
            incident_metadata={  # CHANGED
                "region": random.choice(["us-east-1", "us-west-2", "eu-west-1"]),
                "environment": "production"
            }
        )

        
        db.add(incident)
    
    db.commit()
    print(f"✅ Seeded {len(sample_incidents)} incidents")
    db.close()

if __name__ == "__main__":
    seed_incidents()
