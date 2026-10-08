from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def create_access_token(subject: str, roles: list[str]):
    payload = {
        "sub": subject,
        "roles": roles,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc


def require_role(role: str):
    def dependency(user=Depends(get_current_user)):
        if role not in user.get("roles", []):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return dependency
