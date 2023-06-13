from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from model import User
from schemas import UserAuth, UserCreate


# CryptContext for hashing and verifying API keys
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def genereate_api_key():
    """Generate a 10 character random API key and returns it"""
    import secrets

    return secrets.token_urlsafe(32)[:10]

def check_user(db: Session, username: str):
    """Check if user exists in database"""
    user = db.query(User).filter(User.username == username).first()
    return user is not None

def get_users(db: Session):
    return db.query(User).all()

def user_register(db: Session, username: str, email: str):
    """Register a new user in the database
    This funtion takes a username and email as input and stores it in the database
    It generate a new API key and hash it before storing it in the database
    Expiry date is set to 1 year from the current date

    Returns the API key
    """
    key = genereate_api_key()
    hashed_key = pwd_context.hash(key)
    expiry = datetime.now() + timedelta(days=365)
    db_user = User(username=username, email=email, expire_date=expiry, api_key=hashed_key)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return 

def check_expiry(db: Session, api_key: str):
    """Check if API key has expired"""
    users = db.query(User).all()
    for user in users:
        if pwd_context.verify(api_key, user.api_key):
            user = user
            break
    if user is None:
        return False
    if user.expire_date < datetime.now():
        return False
    return True

def check_api_key(db: Session, key: str):
    """Check if API key exists in database"""
    try:
        users = db.query(User).all()
        for user in users:
            if pwd_context.verify(key, user.api_key):
                return True
        return False
    except:
        return False

def key_details(db: Session, key: str):
    """Get details of API key"""
    users = db.query(User).all()
    for user in users:
        if pwd_context.verify(key, user.api_key):
            return user
    return None