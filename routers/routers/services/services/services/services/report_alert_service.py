from datetime import datetime

report_alerts = []


def acknowledge_alert(alert_index: int):
    if alert_index < 0 or alert_index >= len(report_alerts):
        return None

    report_alerts[alert_index]["status"] = "ACKNOWLEDGED"
    report_alerts[alert_index]["acknowledged_at"] = (
        datetime.utcnow().isoformat()
    )

    return report_alerts[alert_index]


def resolve_alert(alert_index: int):
    if alert_index < 0 or alert_index >= len(report_alerts):
        return None

    report_alerts[alert_index]["status"] = "RESOLVED"
    report_alerts[alert_index]["resolved_at"] = (
        datetime.utcnow().isoformat()
    )

    return report_alerts[alert_index]
