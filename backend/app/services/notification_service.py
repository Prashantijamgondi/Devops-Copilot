import httpx
from app.config import get_settings
from app.models.incident import Incident

settings = get_settings()

class NotificationService:
    """Send notifications to external channels"""
    
    @staticmethod
    async def send_incident_update(incident: Incident):
        """Send incident notification to Slack"""
        if not settings.SLACK_WEBHOOK_URL:
            return
        
        color = {
            "critical": "#FF0000",
            "high": "#FFA500",
            "medium": "#FFFF00",
            "low": "#00FF00"
        }.get(incident.severity.value, "#808080")
        
        status_emoji = {
            "detected": "🔍",
            "analyzing": "🤔",
            "resolving": "⚙️",
            "resolved": "✅",
            "failed": "❌"
        }.get(incident.status.value, "❓")
        
        payload = {
            "attachments": [{
                "color": color,
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{status_emoji} Incident #{incident.id}: {incident.title}"
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": f"*Service:*\n{incident.service_name}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Severity:*\n{incident.severity.value.upper()}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Status:*\n{incident.status.value.title()}"
                            },
                            {
                                "type": "mrkdwn",
                                "text": f"*Error Type:*\n{incident.error_type}"
                            }
                        ]
                    }
                ]
            }]
        }
        
        if incident.root_cause:
            payload["attachments"][0]["blocks"].append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Root Cause:*\n{incident.root_cause}"
                }
            })
        
        if incident.resolution_steps:
            steps = "\n".join([f"• {step}" for step in incident.resolution_steps])
            payload["attachments"][0]["blocks"].append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Resolution Steps:*\n{steps}"
                }
            })
        
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    settings.SLACK_WEBHOOK_URL,
                    json=payload,
                    timeout=10.0
                )
            except Exception as e:
                print(f"Failed to send Slack notification: {e}")
