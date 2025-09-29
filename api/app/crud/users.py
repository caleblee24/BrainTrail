from sqlalchemy.orm import Session
from ..models import User
from ..core.security import hash_password, verify_password

def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create(db: Session, email: str, password: str):
    user = User(email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate(db: Session, email: str, password: str):
    user = get_by_email(db, email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None
