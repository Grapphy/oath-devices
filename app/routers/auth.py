import jwt
import pyotp

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import db_memory
from app.settings import ServerConstraits

router = APIRouter()


class AuthenticationData(BaseModel):
    username: str
    password: str
    code: str = None


@router.post("/api/v1/auth")
def authenticate(authentication_data: AuthenticationData):
    db_user = db_memory.get_user_by_username(username=authentication_data.username)

    if db_user and db_user.password == authentication_data.password:
        if db_user.mfa_enabled:
            if authentication_data.code:
                totp_device = pyotp.TOTP(db_user.oath_secret)
                totp_code = totp_device.now()

                if totp_code == authentication_data.code:
                    return {
                        "access_token": jwt.encode(
                            {"id": db_user.id, "full_name": db_user.name, "mfa": True},
                            ServerConstraits.SECRET_KEY,
                            algorithm=ServerConstraits.ENCRYPTION_ALG
                        )
                    }
            
            raise HTTPException(status_code=401, detail="MFA is required")

        return {
			"access_token": jwt.encode(
				{"id": db_user.id, "full_name": db_user.name, "mfa": False},
				ServerConstraits.SECRET_KEY,
                algorithm=ServerConstraits.ENCRYPTION_ALG
			)
		}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/api/v1/signup")
def signup(authentication_data: AuthenticationData):
    db_user = db_memory.get_user_by_username(username=authentication_data.username)

    if db_user:
        raise HTTPException(status_code=403, detail="User with username {} already exists".format(authentication_data.username))
    
    return db_memory.create_user(username=authentication_data.username, password=authentication_data.password)