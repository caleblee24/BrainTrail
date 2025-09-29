from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .db import SessionLocal
from .core.security import ALGORITHM
from .core.config import settings
from .models import User

reusable_oauth2 = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(reusable_oauth2),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token.credentials, settings.API_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception
    return user
