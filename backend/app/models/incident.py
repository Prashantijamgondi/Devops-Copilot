# from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, JSON, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime
# import enum

# Base = declarative_base()

# class SeverityLevel(str, enum.Enum):
#     CRITICAL = "critical"
#     HIGH = "high"
#     MEDIUM = "medium"
#     LOW = "low"

# class IncidentStatus(str, enum.Enum):
#     DETECTED = "detected"
#     ANALYZING = "analyzing"
#     RESOLVING = "resolving"
#     RESOLVED = "resolved"
#     FAILED = "failed"

# class Incident(Base):
#     __tablename__ = "incidents"
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(255), nullable=False)
#     description = Column(Text)
#     severity = Column(Enum(SeverityLevel), default=SeverityLevel.MEDIUM)
#     status = Column(Enum(IncidentStatus), default=IncidentStatus.DETECTED)
    
#     # Source information
#     source = Column(String(100))  # e.g., "api", "logs", "metrics"
#     service_name = Column(String(100))
#     error_type = Column(String(100))
    
#     # Metadata
#     metadata = Column(JSON, default={})
#     stack_trace = Column(Text)
    
#     # Resolution
#     root_cause = Column(Text)
#     resolution_steps = Column(JSON, default=[])
#     resolution_code = Column(Text)
    
#     # Timestamps
#     detected_at = Column(DateTime, default=datetime.utcnow)
#     resolved_at = Column(DateTime, nullable=True)
    
#     # Relationships
#     actions = relationship("IncidentAction", back_populates="incident")
    
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "description": self.description,
#             "severity": self.severity.value,
#             "status": self.status.value,
#             "source": self.source,
#             "service_name": self.service_name,
#             "error_type": self.error_type,
#             "metadata": self.metadata,
#             "root_cause": self.root_cause,
#             "resolution_steps": self.resolution_steps,
#             "detected_at": self.detected_at.isoformat(),
#             "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None
#         }

# class IncidentAction(Base):
#     __tablename__ = "incident_actions"
    
#     id = Column(Integer, primary_key=True, index=True)
#     incident_id = Column(Integer, ForeignKey("incidents.id"))
    
#     action_type = Column(String(50))  # "analysis", "rollback", "scale", "code_fix"
#     description = Column(Text)
#     result = Column(JSON)
#     success = Column(Integer, default=0)  # 0=pending, 1=success, -1=failed
    
#     created_at = Column(DateTime, default=datetime.utcnow)
    
#     incident = relationship("Incident", back_populates="actions")

# class KnowledgeBase(Base):
#     __tablename__ = "knowledge_base"
    
#     id = Column(Integer, primary_key=True, index=True)
#     incident_id = Column(Integer, ForeignKey("incidents.id"))
    
#     error_pattern = Column(Text)
#     solution = Column(Text)
#     embedding = Column(JSON)  # Vector embedding for similarity search
#     success_rate = Column(Integer, default=0)
    
#     created_at = Column(DateTime, default=datetime.utcnow)

from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class SeverityLevel(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class IncidentStatus(str, enum.Enum):
    DETECTED = "detected"
    ANALYZING = "analyzing"
    RESOLVING = "resolving"
    RESOLVED = "resolved"
    FAILED = "failed"

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(Enum(SeverityLevel), default=SeverityLevel.MEDIUM)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.DETECTED)
    
    # Source information
    source = Column(String(100))  # e.g., "api", "logs", "metrics"
    service_name = Column(String(100))
    error_type = Column(String(100))
    
    # FIXED: Changed 'metadata' to 'incident_metadata'
    incident_metadata = Column(JSON, default={})
    stack_trace = Column(Text)
    
    # Resolution
    root_cause = Column(Text)
    resolution_steps = Column(JSON, default=[])
    resolution_code = Column(Text)
    
    # Timestamps
    detected_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    actions = relationship("IncidentAction", back_populates="incident")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "status": self.status.value,
            "source": self.source,
            "service_name": self.service_name,
            "error_type": self.error_type,
            "metadata": self.incident_metadata,  # Still return as 'metadata' in API
            "root_cause": self.root_cause,
            "resolution_steps": self.resolution_steps,
            "detected_at": self.detected_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None
        }

class IncidentAction(Base):
    __tablename__ = "incident_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    
    action_type = Column(String(50))  # "analysis", "rollback", "scale", "code_fix"
    description = Column(Text)
    result = Column(JSON)
    success = Column(Integer, default=0)  # 0=pending, 1=success, -1=failed
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    incident = relationship("Incident", back_populates="actions")

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    
    error_pattern = Column(Text)
    solution = Column(Text)
    embedding = Column(JSON)  # Vector embedding for similarity search
    success_rate = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
