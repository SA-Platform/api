import datetime
from fastapi import HTTPException, status
from datetime import timedelta
from jose import jwt, JWTError

SECRET_KEY = "1e0788a28e2e503315a3a894d353abaa36ace075faae8650f714d7c880f01da5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_token(payload: dict, duration: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    payload["exp"] = datetime.datetime.now() + timedelta(minutes=duration)
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
