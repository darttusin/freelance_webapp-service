import uuid
import hashlib
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta

from app.database.users_db import get_user_by_email
from app.database.admins_db import get_admin_by_email
from app.schemas.users_schemas import UserLogin as User

import app.constants.constants as const

from app.utils.users_utils import verify_password


async def authenticate_user(
    user_email: str, 
    password: str
):
    user = await get_user_by_email(user_email)
    if not user:
        return False
    if not verify_password(
        password, 
        user['user_password']
    ):
        return False
    return user


async def authenticate_admin(
    admin_email: str, 
    password: str
):
    admin = await get_admin_by_email(admin_email)
    if not admin:
        return False
    if not verify_password(
        password, 
        admin['admin_password']
    ):
        return False
    return admin


async def get_current_admin(
    token: str = Depends(const.oauth2_scheme_admin)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token, 
            const.SECRET_KEY, 
            algorithms=[const.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None: raise credentials_exception

    except JWTError:
        raise credentials_exception
        
    admin = await get_admin_by_email(username)
    if admin is None:
        raise credentials_exception
    return admin


async def get_current_user(
    token: str = Depends(const.oauth2_scheme)
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token, 
            const.SECRET_KEY, 
            algorithms=[const.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None: raise credentials_exception

    except JWTError:
        raise credentials_exception
        
    user = await get_user_by_email(username)
    if user is None:
        raise credentials_exception
    return user