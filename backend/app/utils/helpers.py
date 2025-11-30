from datetime import datetime
from typing import Optional

def calculate_duration(start: datetime, end: Optional[datetime]) -> float:
    """Calculate duration in minutes between two timestamps"""
    if not end:
        end = datetime.utcnow()
    return (end - start).total_seconds() / 60

def format_error_message(error: Exception) -> str:
    """Format exception for logging"""
    return f"{error.__class__.__name__}: {str(error)}"

def extract_service_from_url(url: str) -> str:
    """Extract service name from URL"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.split('.')[0]
    except:
        return "unknown"

def severity_to_priority(severity: str) -> int:
    """Convert severity to numeric priority"""
    mapping = {
        "critical": 1,
        "high": 2,
        "medium": 3,
        "low": 4
    }
    return mapping.get(severity.lower(), 3)
