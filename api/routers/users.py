from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.db.models.core_models import User
from api.dependencies import get_db, get_current_user
from api.utils import create_token
from api.validators import UserValidator, UsernameValidator, HTTPError

usersRouter: APIRouter = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@usersRouter.get(path="/all")
async def get_users(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(User).all()


@usersRouter.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: UserValidator, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=request.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    new_user: User = User(**request.model_dump())
    db.add(new_user)
    db.commit()
    return {"access_token": create_token({"username": new_user.username}), "token_type": "bearer"}


@usersRouter.post("/signin")
async def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: User | None = db.query(User).filter(
        (User.email == form_data.username) | (User.username == form_data.username)).first()
    if user:
        if user.check_password(form_data.password):
            return {"access_token": create_token({"username": user.username}), "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect password")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="user not found")  # for debugging only, should be changed to raise unauthorized always


@usersRouter.post("/check-username",
                  responses={
                      status.HTTP_409_CONFLICT: {"model": HTTPError, "description": "username not available"}
                  })
async def validate_username(request: UsernameValidator, db: Session = Depends(get_db)):  ##### need to change the validation error msg
    existing_user = db.query(User).filter_by(username=request.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username is taken")
    return {"message": "username is available"}

# @app.post("/check-email")
# async def validate_email(email: EmailStr, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter_by(email=email).first()
#     if existing_user:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
#     return {"message": "Email is available"}