import jwt

from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader
from database import db_memory

router = APIRouter()

token_header = APIKeyHeader(name="X-Auth-Token")

def verify_token_header(token_header: str = Security(token_header)) -> dict:
    try:
        decoded_token = jwt.decode(token_header, "128FH8ASDVHNI3NFMKSDFMKDSFSFDFSAD", algorithms="HS256")
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


@router.get("/api/v1/@me")
def get_self_profile(current_user: dict = Security(verify_token_header)):
    return {
        "id": current_user.get("id"),
        "name": current_user.get("full_name")
    }