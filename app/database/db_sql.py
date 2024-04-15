from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


engine = create_engine('mysql://root:secret@api-mysql/demo_oath')
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    oath_secret = Column(String(255), default=None)
    mfa_enabled = Column(Boolean, default=False)

# Define the BackupCode model
class BackupCode(Base):
    __tablename__ = 'backup_codes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    backup_code = Column(String(255))

# Function to retrieve a user by ID
def get_user_by_id(session: Session, user_id):
    return session.query(User).filter(User.id == user_id).first()

# Function to retrieve a user by username
def get_user_by_username(session: Session, username):
    return session.query(User).filter(User.username == username).first()

# Function to search for backup code
def get_backup_code(session: Session, backup_code: str):
    return session.query(BackupCode).filter(BackupCode.backup_code == backup_code).first()

# Function to create a new user
def create_user(session: Session, username, password):
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    return new_user

# Function to patch a user
def patch_user(session: Session, patched_user: User):
    session.add(patched_user)
    session.commit()
    return patched_user

# Function to save backup codes
def create_backup_codes(session: Session, user_id: int, backup_codes: list):
    for backup_code in backup_codes:
        new_backup_code = BackupCode(user_id=user_id, backup_code=backup_code)
        session.add(new_backup_code)
    session.commit()
    return True

# Function to remove a used backup code
def delete_backup_code(session: Session, backup_code: str):
    session.delete(backup_code)
    session.commit()
    return True


# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)