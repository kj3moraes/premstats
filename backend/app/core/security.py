from app.core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic_settings import BaseSettings
from starlette.status import HTTP_403_FORBIDDEN

security = HTTPBearer()


def verify_add_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != settings.ADD_ACCESS_TOKEN:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid or expired token."
        )
    return credentials.credentials


def verify_update_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != settings.UPDATE_ACCESS_TOKEN:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid or expired token."
        )
    return credentials.credentials


def verify_delete_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != settings.DELETE_ACCESS_TOKEN:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Invalid or expired token."
        )
    return credentials.credentials
