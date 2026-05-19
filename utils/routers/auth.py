from fastapi import APIRouter, HTTPException

from utils.notification_service import send_security_alert
from utils.account_lock import (
    lock_account,
    is_account_locked
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

VALID_USERS = {
    "admin": "admin123"
}


@router.post("/login")
def login(username: str, password: str):

    if is_account_locked(username):

        send_security_alert(
            username=username,
            event_type="ACCOUNT_LOCKED"
        )

        raise HTTPException(
            status_code=403,
            detail="Account temporarily locked."
        )

    if username not in VALID_USERS or VALID_USERS[username] != password:

        send_security_alert(
            username=username,
            event_type="FAILED_LOGIN_ATTEMPT"
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "message": "Login successful"
    }
