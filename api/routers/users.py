from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.routers.features_base import User
from api.dependencies import get_db, get_current_user
from api.utils import create_token
from api.validators import UsernameValidator, HTTPErrorValidator

usersRouter: APIRouter = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@usersRouter.get(path="/all")
async def get_users(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return User.get_db_dump(db)


@usersRouter.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: User.validator, db: Session = Depends(get_db)):
    if User.get_db_first(db, "email", request.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    request.username = request.username.username
    User.validate_username(db, request.username)
    User.create(request, db)
    return {"access_token": create_token({"username": request.username}), "token_type": "bearer"}


@usersRouter.post("/signin")
async def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = User.get_db_username_or_email(db, form_data.username)
    if user:
        if user.check_password(form_data.password):
            return {"access_token": create_token({"username": user.username}), "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect password")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="user not found")  # for debugging only, should be changed to raise unauthorized always


@usersRouter.post("/check-username",
                  responses={
                      status.HTTP_409_CONFLICT: {"model": HTTPErrorValidator, "description": "username not available"}
                  })
async def validate_username(request: UsernameValidator,
                            db: Session = Depends(get_db)):  ##### need to change the validation error msg
    User.validate_username(db, request.username)
    return {"message": "username is available"}
