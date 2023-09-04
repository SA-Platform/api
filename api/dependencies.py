from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api.db import SessionLocal
from api.db.models import UserModel  # unresolved reference ignored
from api.utils import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/signin")


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    user = db.query(UserModel).filter_by(username=payload.get("username")).first()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User in token is not found",  # debugging only
        headers={"WWW-Authenticate": "Bearer"},
    )
