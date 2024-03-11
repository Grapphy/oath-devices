from fastapi import APIRouter, HTTPException

from database import db_memory

router = APIRouter()


@router.get("/api/v1/users/{user_id}")
def get_user_profile(user_id: str):
    db_user = db_memory.get_user_by_id(user_id=user_id)

    if db_user:
        return {
            "id": db_user.id,
            "name": db_user.name
        }

    raise HTTPException(status_code=404, detail="User does not exist")


@router.get("/api/v1/users/me")
def get_self_profile():
    return {
        "id": "me",
        "name": "User me"
    }