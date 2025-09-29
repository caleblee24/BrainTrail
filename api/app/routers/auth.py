from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import UserCreate, Token
from ..crud import users as users_crud
from ..core.security import create_access_token
from ..deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if users_crud.get_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    users_crud.create(db, payload.email, payload.password)
    token = create_access_token(payload.email)
    return {"access_token": token}

@router.post("/login", response_model=Token)
def login(payload: UserCreate, db: Session = Depends(get_db)):
    user = users_crud.authenticate(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(user.email)
    return {"access_token": token}
