from sqlalchemy.orm import Session
from datetime import datetime
import asyncio

from app.models.incident import Incident, IncidentAction, IncidentStatus, SeverityLevel
from app.services.database import SessionLocal
from app.services.ai_agent import OumiAgent
from app.services.kestra_service import KestraService
from app.services.notification_service import NotificationService

class IncidentProcessor:
    
    @staticmethod
    async def process_incident(incident_id: int):
        """Main incident processing pipeline"""
        db = SessionLocal()
        try:
            incident = db.query(Incident).filter(Incident.id == incident_id).first()
            if not incident:
                return
            
            # Step 1: Analyze with AI Agent
            print(f"🔍 Analyzing incident #{incident_id}")
            incident.status = IncidentStatus.ANALYZING
            db.commit()
            
            analysis = await IncidentProcessor._analyze_incident(incident)
            
            # Store analysis
            action = IncidentAction(
                incident_id=incident.id,
                action_type="analysis",
                description="AI-powered root cause analysis",
                result=analysis,
                success=1
            )
            db.add(action)
            
            incident.root_cause = analysis.get("root_cause", "Unknown")
            incident.resolution_steps = analysis.get("resolution_steps", [])
            db.commit()
            
            # Step 2: Trigger Kestra workflow for automated resolution
            print(f"⚙️ Triggering resolution workflow for incident #{incident_id}")
            incident.status = IncidentStatus.RESOLVING
            db.commit()
            
            resolution_result = await IncidentProcessor._execute_resolution(incident, analysis)
            
            # Step 3: Verify resolution
            if resolution_result.get("success"):
                incident.status = IncidentStatus.RESOLVED
                incident.resolved_at = datetime.utcnow()
                
                # Add to knowledge base
                await IncidentProcessor._add_to_knowledge_base(incident, analysis)
            else:
                incident.status = IncidentStatus.FAILED
            
            db.commit()
            
            # Step 4: Send notifications
            await NotificationService.send_incident_update(incident)
            
            print(f"✅ Incident #{incident_id} processed successfully")
            
        except Exception as e:
            print(f"❌ Error processing incident #{incident_id}: {str(e)}")
            incident.status = IncidentStatus.FAILED
            db.commit()
        finally:
            db.close()
    
    @staticmethod
    async def _analyze_incident(incident: Incident) -> dict:
        """Analyze incident using Oumi AI agent"""
        agent = OumiAgent()
        
        context = {
            "title": incident.title,
            "description": incident.description,
            "service": incident.service_name,
            "error_type": incident.error_type,
            "stack_trace": incident.stack_trace,
            "metadata": incident.incident_metadata  # CHANGED
        }
        
        analysis = await agent.analyze_incident(context)
        return analysis
    
    @staticmethod
    async def _execute_resolution(incident: Incident, analysis: dict) -> dict:
        """Execute automated resolution via Kestra"""
        kestra = KestraService()
        
        workflow_input = {
            "incident_id": incident.id,
            "service_name": incident.service_name,
            "resolution_steps": analysis.get("resolution_steps", []),
            "severity": incident.severity.value
        }
        
        result = await kestra.trigger_workflow(
            "incident-resolution",
            workflow_input
        )
        
        return result
    
    @staticmethod
    async def _add_to_knowledge_base(incident: Incident, analysis: dict):
        """Add incident solution to knowledge base for future reference"""
        from app.models.incident import KnowledgeBase
        from app.services.embedding_service import EmbeddingService
        
        db = SessionLocal()
        try:
            embedding_service = EmbeddingService()
            
            # Create embedding of error pattern
            error_pattern = f"{incident.error_type}: {incident.description}"
            embedding = await embedding_service.create_embedding(error_pattern)
            
            kb_entry = KnowledgeBase(
                incident_id=incident.id,
                error_pattern=error_pattern,
                solution=incident.root_cause,
                embedding=embedding,
                success_rate=100  # Will be updated based on feedback
            )
            
            db.add(kb_entry)
            db.commit()
        finally:
            db.close()
    
    @staticmethod
    async def create_from_logs(log_payload: dict):
        """Create incident from log entry"""
        db = SessionLocal()
        try:
            incident = Incident(
                title=f"Error in {log_payload.get('service', 'Unknown Service')}",
                description=log_payload.get("message", ""),
                severity=SeverityLevel.MEDIUM,
                source="logs",
                service_name=log_payload.get("service", "unknown"),
                error_type="log_error",
                incident_metadata=log_payload  # CHANGED
            )
            db.add(incident)
            db.commit()
            db.refresh(incident)
            
            await IncidentProcessor.process_incident(incident.id)
        finally:
            db.close()
    
    @staticmethod
    async def create_from_metrics(metrics_payload: dict):
        """Create incident from metrics threshold breach"""
        db = SessionLocal()
        try:
            incident = Incident(
                title=f"Threshold breach: {metrics_payload.get('metric_name')}",
                description=f"Value {metrics_payload.get('value')} exceeded threshold {metrics_payload.get('threshold')}",
                severity=SeverityLevel.HIGH,
                source="metrics",
                service_name=metrics_payload.get("service", "unknown"),
                error_type="threshold_breach",
                incident_metadata=metrics_payload  # CHANGED
            )
            db.add(incident)
            db.commit()
            db.refresh(incident)
            
            await IncidentProcessor.process_incident(incident.id)
        finally:
            db.close()
