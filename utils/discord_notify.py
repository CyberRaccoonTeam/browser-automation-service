"""
Discord Webhook Notifications for Browser Automation Service
"""
import requests
from datetime import datetime

# Discord webhook URL for deployments
WEBHOOK_URL = "https://discord.com/api/webhooks/1480530664125239306/zlYI-PWkcYwdyvOFwXW0jtKFkM1-VflpAA0o0NMFrdOsWNVqgz9euUyWTjAvh9sSG8pN"


def send_notification(title, message, color=0x00ff41, fields=None):
    """Send a notification to Discord"""
    
    embed = {
        "title": title,
        "description": message,
        "color": color,
        "footer": {"text": "🦝 Browser Automation Service"},
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if fields:
        embed["fields"] = fields
    
    payload = {"embeds": [embed]}
    
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
        return True
    except Exception as e:
        print(f"Discord notification failed: {e}")
        return False


def notify_task_created(task_id, task_type, url):
    """Notify when a new task is created"""
    return send_notification(
        title="🤖 Browser Task Created",
        message=f"New automation task submitted",
        color=0x3498db,
        fields=[
            {"name": "Task ID", "value": task_id, "inline": True},
            {"name": "Type", "value": task_type.upper(), "inline": True},
            {"name": "URL", "value": url[:80] if len(url) > 80 else url, "inline": False}
        ]
    )


def notify_task_completed(task_id, task_type, duration_seconds):
    """Notify when a task completes"""
    return send_notification(
        title="✅ Browser Task Completed",
        message=f"Automation task finished successfully",
        color=0x00ff41,
        fields=[
            {"name": "Task ID", "value": task_id, "inline": True},
            {"name": "Type", "value": task_type.upper(), "inline": True},
            {"name": "Duration", "value": f"{duration_seconds:.1f}s", "inline": True}
        ]
    )


def notify_task_failed(task_id, error_message):
    """Notify when a task fails"""
    return send_notification(
        title="❌ Browser Task Failed",
        message=f"Automation task encountered an error",
        color=0xff4444,
        fields=[
            {"name": "Task ID", "value": task_id, "inline": True},
            {"name": "Error", "value": error_message[:200] if len(error_message) > 200 else error_message, "inline": False}
        ]
    )


def notify_milestone(total_tasks, milestone):
    """Notify on usage milestones"""
    return send_notification(
        title="📊 Usage Milestone",
        message=f"Browser Automation Service hit **{milestone}** total tasks!",
        color=0x9b59b6,
        fields=[
            {"name": "Total Tasks", "value": str(total_tasks), "inline": True}
        ]
    )


def notify_startup(port):
    """Notify when API starts up"""
    return send_notification(
        title="🚀 Browser Automation Service Online",
        message=f"API is now running on port {port}",
        color=0x00ff41,
        fields=[
            {"name": "Health Check", "value": f"http://localhost:{port}/health", "inline": False}
        ]
    )