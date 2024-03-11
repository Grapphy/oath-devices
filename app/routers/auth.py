import uuid
from fastapi import APIRouter, HTTPException

from database import db_memory

router = APIRouter()


@router.post("/api/v1/auth")
def authenticate(username: str, password: str):
    db_user = db_memory.get_user_by_username(username=username)

    if db_user and db_user.password == password:
        return {
            "token": f"{db_user.name}-{db_user.id}-{str(uuid.uuid4())}",
            "user": {
                "id": db_user.id,
                "name": db_user.name
            }
        }
    
    raise HTTPException(status_code=401, detail="Invalid credentials")
