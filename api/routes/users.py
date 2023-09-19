from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.const import CorePermissions, FeaturePermissions
from api.crud.core.role import Role
from api.crud.core.user import User
from api.crud.core.userdivisionpermission import UserDivisionPermission
from api.db.models import UserModel, RoleModel, UserRoleModel
from api.dependencies import get_db, CheckPermission
from api.utils import create_token, decode_permissions
from api.validators import UserValidator, UsernameValidator, FeaturePermissionValidator, CorePermissionValidator, \
    HTTPErrorValidator

usersRouter: APIRouter = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@usersRouter.get(path="/all")
async def get_users(db: Session = Depends(get_db)):
    return User.get_db_dump(db)


@usersRouter.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: UserValidator, db: Session = Depends(get_db)):
    if User.get_db_first(db, "email", request.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    User.validate_username(db, request.username)
    User.create(db, **request.model_dump())
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


@usersRouter.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db),
                      _: UserModel = Depends(CheckPermission(CorePermissions.DELETE_USER, core=True))):
    return User.delete(user_id, db)


@usersRouter.get("/users_with_special_permissions")
async def get_users_with_divisions_permissions(db: Session = Depends(get_db)):
    return UserDivisionPermission.get_db_dump(db)


@usersRouter.post("/assign_user_special_permissions")
async def assign_user_division_permissions(user_id: int, division_id: int, request: FeaturePermissionValidator,
                                           db: Session = Depends(get_db)):
    return  UserDivisionPermission.create(db, user_id, division_id, **request.model_dump())


@usersRouter.delete("/delete_user_special_permissions/{user_id}/{division_id}")
async def delete_user_division_permissions(user_id: int, division_id: int, db: Session = Depends(get_db)):
    return UserDivisionPermission.delete(db, user_id, division_id)


@usersRouter.get("/get_user_permissions/{user_id}")
async def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    return decode_permissions(User.get_db_first(db, "id", user_id).permissions, list(CorePermissions))


@usersRouter.post("/assign_user_permissions")
async def assign_user_permissions(user_id: int, request: CorePermissionValidator, db: Session = Depends(get_db)):
    return User.edit_user_permissions(db, user_id, **request.model_dump())


@usersRouter.post("/assign_user_role")
async def assign_user_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    role = Role.get_db_first(db, "id", role_id)
    if role: UserDivisionPermission.create(db, user_id, role.division_id, **{
        "permissions": decode_permissions(0, list(FeaturePermissions))})
    return User.assign_user_role(db, user_id, role_id)


@usersRouter.get("/get_user_roles/{user_id}")
async def get_user_roles(user_id: int, db: Session = Depends(get_db)):
    user_roles = (
        db.query(RoleModel.name)
        .join(UserRoleModel, RoleModel.id == UserRoleModel.role_id)
        .filter(UserRoleModel.user_id == user_id)
        .all()
    )
    return [role[0] for role in user_roles]


@usersRouter.post("/assign_user_to_division/{user_id}/{division_id}")
async def assign_user_to_division(user_id: int, division_id: int, db: Session = Depends(get_db)):
    return UserDivisionPermission.create(db, user_id, division_id, **{"permissions": 0})
