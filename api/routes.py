
from typing import Union

from fastapi import FastAPI, status, Depends

from api.validators import UserValidator
from api.database.models import User
from api import SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup", tags=["Users"])
async def signup(request: UserValidator, db: Session = Depends(get_db)):
    new_user = User(**request.model_dump())
    db.add(new_user)
    db.commit()
    return new_user



