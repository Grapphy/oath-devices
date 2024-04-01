import jwt

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import db_memory

router = APIRouter()


class AuthenticationData(BaseModel):
    username: str
    password: str


@router.post("/api/v1/auth")
def authenticate(authentication_data: AuthenticationData):
    db_user = db_memory.get_user_by_username(username=authentication_data.username)

    if db_user and db_user.password == authentication_data.password:
        return {
			"access_token": jwt.encode(
				{"id": db_user.id, "full_name": db_user.name},
				"128FH8ASDVHNI3NFMKSDFMKDSFSFDFSAD",
                algorithm="HS256"
			)
		}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/api/v1/signup")
def signup(authentication_data: AuthenticationData):
    db_user = db_memory.get_user_by_username(username=authentication_data.username)

    if db_user:
        raise HTTPException(status_code=403, detail="User with username {} already exists".format(authentication_data.username))
    
    return db_memory.create_user(username=authentication_data.username, password=authentication_data.password)