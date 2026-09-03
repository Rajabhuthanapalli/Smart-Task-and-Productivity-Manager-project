from datetime import datetime, timedelta

ESCALATION_THRESHOLD_HOURS = 24


def check_escalation(alert):
    created_at = datetime.fromisoformat(alert["created_at"])

    age = datetime.utcnow() - created_at

    if (
        alert["status"] == "OPEN"
        and age >= timedelta(hours=ESCALATION_THRESHOLD_HOURS)
    ):
        alert["status"] = "ESCALATED"
        alert["escalated_at"] = datetime.utcnow().isoformat()
        alert["escalation_reason"] = (
            "Alert remained unresolved beyond threshold"
        )

    return alert
