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


# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)