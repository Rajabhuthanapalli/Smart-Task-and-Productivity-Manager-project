from services.email_report_service import send_report_email


def notify_report_failure(
    recipient: str,
    report_name: str,
    error_message: str,
    retry_count: int
):
    subject = f"Report Failure Alert - {report_name}"

    message = (
        f"Scheduled report execution failed.\n\n"
        f"Report: {report_name}\n"
        f"Retry Count: {retry_count}\n"
        f"Error: {error_message}\n"
    )

    return send_report_email(
        recipient=recipient,
        report_name=subject
    )
