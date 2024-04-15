import jwt
from .database.db_sql import SessionLocal
from .settings import ServerConstraits


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_user_token(db_user, is_mfa: bool = False):
    {
        "access_token": jwt.encode({
            "id": db_user.id, "username": db_user.username, "mfa": is_mfa},
            ServerConstraits.SECRET_KEY,
            algorithm=ServerConstraits.ENCRYPTION_ALG
        )
    }