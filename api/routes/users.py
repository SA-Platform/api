from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.const import CorePermissions, FeaturePermissions
from api.crud.core.role import Role
from api.crud.core.user import User
from api.crud.core.userroledivisionpermission import UserRoleDivisionPermission
from api.db.models import UserModel, RoleModel, UserRoleModel
from api.dependencies import get_db, CheckPermission
from api.utils import create_token, decode_permissions
from api.validators import UserValidator, UsernameValidator, FeaturePermissionValidator, CorePermissionValidator, \
    HTTPErrorValidator, AssignToDivisionValidator

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


@usersRouter.get("/users_assigned_to_divisions")
async def get_users_with_divisions_permissions(db: Session = Depends(get_db)):
    return UserRoleDivisionPermission.get_db_dump(db)


@usersRouter.get("/get_user_in_division/{division_id}")
async def get_users_in_division(division_id: int, db: Session = Depends(get_db)):
    records = UserRoleDivisionPermission.get_db_all(db, "division_id", division_id)
    return [record.user for record in records]


@usersRouter.post("/assign_user_division_permissions")
async def assign_user_division_permissions(user_id: int, division_id: int, request: FeaturePermissionValidator,
                                           db: Session = Depends(get_db)):
    return UserRoleDivisionPermission.create(db, user_id, division_id, role_id=None, **request.model_dump())


@usersRouter.delete("/delete_user_special_permissions/{user_id}/{division_id}")
async def delete_user_division_permissions(user_id: int, division_id: int, db: Session = Depends(get_db)):
    return UserRoleDivisionPermission.delete(db, user_id, division_id, role_id=None)


@usersRouter.get("/get_user_permissions/{user_id}")
async def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    return decode_permissions(User.get_db_first(db, "id", user_id).permissions, list(CorePermissions))


@usersRouter.post("/assign_user_permissions")
async def assign_user_permissions(user_id: int, request: CorePermissionValidator, db: Session = Depends(get_db)):
    return User.edit_user_permissions(db, user_id, **request.model_dump())


@usersRouter.post("/assign_user_role")
async def assign_user_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    role = Role.get_db_first(db, "id", role_id)
    if role:
        try:
            UserRoleDivisionPermission.create(db, user_id, role.division_id, role_id,
                                              **decode_permissions(0, list(FeaturePermissions)))
        except HTTPException:
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This role does not exist in any division")
    return User.assign_user_role(db, user_id, role_id)


@usersRouter.delete("/delete_user_role/{user_id}/{role_id}")
async def delete_user_role(user_id: int, division_id: int, role_id: int, db: Session = Depends(get_db)):
    return UserRoleDivisionPermission.delete(db, user_id=user_id, role_id=role_id,
                                             division_id=division_id)


@usersRouter.get("/get_user_roles/{user_id}")
async def get_user_roles(user_id: int, db: Session = Depends(get_db)):
    user_roles = (
        db.query(UserRoleDivisionPermission)
        .filter_by(user_id=user_id)
        .all()
    )
    return [role for role in user_roles]


@usersRouter.post("/assign_user_to_division/{user_id}/{division_id}")
async def assign_user_to_division(request: AssignToDivisionValidator, user_id: int, division_id: int,
                                  db: Session = Depends(get_db)):
    role = Role.get_db_first(db, "id", request.role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return UserRoleDivisionPermission.create(db, user_id, division_id, request.role_id,
                                             **decode_permissions(0, list(FeaturePermissions)))
