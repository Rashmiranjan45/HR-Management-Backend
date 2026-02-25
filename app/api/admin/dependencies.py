
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.api.admin.jwt_handler import verify_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_admin(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = verify_token(token)
        if payload.get("sub") != "admin":
            raise HTTPException(403, "Not admin")
        return payload
    except Exception:
        raise HTTPException(401, "Invalid or expired token")