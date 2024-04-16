import jwt
from datetime import datetime, timedelta

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
    current_time = datetime.utcnow()
    expiration_timedelta = timedelta(minutes=10)
    expiration_date = current_time + expiration_timedelta
    expiration_timestamp = int(expiration_date.timestamp())
    
    claims = {
        "id": db_user.id,
        "username": db_user.username,
        "mfa": is_mfa,
        "expiration": expiration_timestamp
    }

    return {
        "access_token": jwt.encode(
            claims,
            ServerConstraits.SECRET_KEY,
            algorithm=ServerConstraits.ENCRYPTION_ALG
        )
    }