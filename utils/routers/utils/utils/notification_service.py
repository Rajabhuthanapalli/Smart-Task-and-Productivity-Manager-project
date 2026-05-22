from utils.email_service import send_email_alert


def send_security_alert(username: str, event_type: str):

    message = (
        f"Security event detected for user '{username}': "
        f"{event_type}"
    )

    email_response = send_email_alert(
        to_email="admin@smarttaskapp.com",
        subject="Security Alert Notification",
        message=message
    )

    return {
        "username": username,
        "event_type": event_type,
        "notification_status": email_response["status"]
    }
