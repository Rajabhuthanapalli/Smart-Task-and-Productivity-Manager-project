from fastapi import APIRouter, HTTPException

from services.alert_escalation import check_escalation
from services.report_alert_service import report_alerts

router = APIRouter(
    prefix="/report-alerts",
    tags=["Report Alerts"]
)


@router.patch("/{alert_index}/escalate")
def escalate_alert(alert_index: int):

    if alert_index < 0 or alert_index >= len(report_alerts):
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert = check_escalation(report_alerts[alert_index])

    return {
        "message": "Alert escalation check completed",
        "alert": alert
    }
