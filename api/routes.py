from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.validators import UserSignup
from api.db.models import User
from api.utils import get_db, create_token, get_current_user

app: FastAPI = FastAPI()


@app.post("/signup", tags=["Users"], status_code=status.HTTP_201_CREATED)
async def signup(request: UserSignup, db: Session = Depends(get_db)):
    new_user: User = User(**request.model_dump())
    db.add(new_user)
    db.commit()
    return {"access_token": create_token({"username": new_user.username}), "token_type": "bearer"}


@app.post("/signin", tags=["Users"], status_code=status.HTTP_200_OK)
async def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: User | None = db.query(User).filter((User.email == form_data.username) | (User.username == form_data.username)).first()
    if user:
        if user.check_password(form_data.password):
            return {"access_token": create_token({"username": user.username}), "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect password")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="user not found")  # for debugging only, should be changed to raise unauthorized always


@app.get("/getusers", tags=["Users"], status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(User).all()
