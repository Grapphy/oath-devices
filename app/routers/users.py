from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/users/{user_id}")
def get_user_profile(user_id: str):
    return {
        "id": user_id,
        "name": f"User {user_id}"
    }