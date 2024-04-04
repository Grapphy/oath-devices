import jwt
import pyotp

from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from app.database import db_memory
from app.settings import ServerConstraits


router = APIRouter()


class DeviceRegistrationData(BaseModel):
    password: str
    code: str
    secret: str


token_header = APIKeyHeader(name="X-Auth-Token")


def verify_token_header(token_header: str = Security(token_header)) -> dict:
    try:
        decoded_token = jwt.decode(token_header, ServerConstraits.SECRET_KEY, algorithms=ServerConstraits.ENCRYPTION_ALG)
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Invalid token signature")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token error")


@router.get("/api/v1/users/{user_id}")
def get_user_profile(user_id: str):
    db_user = db_memory.get_user_by_id(user_id=user_id)

    if db_user:
        return {
            "id": db_user.id,
            "name": db_user.name
        }

    raise HTTPException(status_code=404, detail="User does not exist")


@router.post("/api/v1/@me/mfa/totp/enable")
def set_authenticator_mfa(device_reg_data: DeviceRegistrationData, current_user: dict = Security(verify_token_header)):
    db_user = db_memory.get_user_by_id(current_user.get("id"))

    if db_user.password == device_reg_data.password:

        if db_user.mfa_enabled:
            raise HTTPException(status_code=403, detail="You already have mfa enabled")

        totp_device = pyotp.TOTP(device_reg_data.secret)
        topt_code = totp_device.now()

        if topt_code == device_reg_data.code:
            db_user.oath_secret = device_reg_data.secret
            db_user.backup_codes = [
                pyotp.random_base32()
                for _ in range(5)
            ]

            db_user.mfa_enabled = True

            return {
                "backup_codes": db_user.backup_codes
            }
        
        raise HTTPException(status_code=404, detail="OTP code does not match")

    raise HTTPException(status_code=404, detail="Invalid password")


@router.post("/api/v1/@me/mfa/totp/disable")
def set_authenticator_mfa(current_user: dict = Security(verify_token_header)):
    db_user = db_memory.get_user_by_id(current_user.get("id"))

    if db_user.mfa_enabled:
        if current_user.get("mfa"):
            db_user.backup_codes = None
            db_user.oath_secret = None
            db_user.mfa_enabled = False
            return {"message": "MFA has been disabled"}
        
        return HTTPException(status_code=403, detail="MFA is required to access this endpoint")
    
    return HTTPException(status_code=403, detail="You do not have MFA enabled")


@router.get("/api/v1/@me")
def get_self_profile(current_user: dict = Security(verify_token_header)):
    db_user = db_memory.get_user_by_id(current_user.get("id"))
    
    return {
        "id": db_user.id,
        "name": db_user.name,
        "mfa_enabled": db_user.mfa_enabled
    }