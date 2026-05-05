from fastapi import Request, HTTPException

VALID_TOKENS = ["abc123", "admin456"]


def verify_token(request: Request):
    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    token = token.replace("Bearer ", "")

    if token not in VALID_TOKENS:
        raise HTTPException(status_code=403, detail="Invalid token")

    return True
