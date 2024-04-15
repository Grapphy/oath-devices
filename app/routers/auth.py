import jwt
import pyotp

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session


# from app.database import db_memory
from ..dependencies import get_db, generate_user_token
from ..database.db_sql import (get_user_by_username, create_user, get_backup_code, delete_backup_code)

router = APIRouter()


class AuthenticationData(BaseModel):
    username: str
    password: str
    code: str = None
    backup_code: str = None


@router.post("/api/v1/auth")
def authenticate(authentication_data: AuthenticationData,  db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=authentication_data.username)

    if db_user and db_user.password == authentication_data.password:
        if db_user.mfa_enabled:
            if authentication_data.code:
                totp_device = pyotp.TOTP(db_user.oath_secret)
                totp_code = totp_device.now()
                if totp_code == authentication_data.code:
                    return generate_user_token(db_user=db_user, is_mfa=True)
                else:
                    raise HTTPException(status_code=401, detail="Invalid OTP code")
            elif authentication_data.backup_code:
                backup_code = get_backup_code(db, backup_code=authentication_data.backup_code)
                if backup_code and backup_code.user_id == db_user.id:
                    delete_backup_code(db, backup_code=backup_code)
                    return generate_user_token(db_user=db_user, is_mfa=True)
                else:
                    raise HTTPException(status_code=401, detail="Invalid backup code")
            
            raise HTTPException(status_code=401, detail="MFA is required")

        return generate_user_token(db_user=db_user)
    
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/api/v1/signup")
def signup(authentication_data: AuthenticationData,  db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=authentication_data.username)

    if db_user:
        raise HTTPException(status_code=403, detail="User with username {} already exists".format(authentication_data.username))
    
    new_user = create_user(db, username=authentication_data.username, password=authentication_data.password)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "mfa": new_user.mfa_enabled
    }