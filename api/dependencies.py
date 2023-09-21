from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Integer
from sqlalchemy.orm import Session, aliased

from api.db import SessionLocal
from api.db.models import UserModel  # unresolved reference ignored
from api.db.models.division_model import DivisionModel
from api.db.models.role_model import RoleModel
from api.db.models.user_division_permission import UserDivisionPermissionModel
from api.db.models.user_role import UserRoleModel
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


class CheckPermission:
    def __init__(self, permission_to_check: int, core: bool = False):
        self.permission_to_check: int = permission_to_check
        self.core: bool = core

    async def __call__(self, request: Request,
                       user: UserModel = Depends(get_current_user),
                       db: Session = Depends(get_db)) -> UserModel:
        if self.core:
            self.check_user_permission(self.permission_to_check, user)
        else:
            division: DivisionModel | None = db.query(DivisionModel).filter_by(
                id=request.path_params["division_id"]).first()
            special_user = self.check_special_user_permission(self.permission_to_check, user, division, db)
            if special_user is not None:
                return special_user
            else:
                # Check role permission
                self.check_role_permission(self.permission_to_check, user, division, db)
                return user

    @staticmethod
    def check_user_permission(permission_to_check: int, user: UserModel) -> UserModel:
        if user.permissions & permission_to_check:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not have permission")

    @staticmethod
    def check_role_permission(permission_to_check: int, user: UserModel, division: DivisionModel,
                              db: Session = Depends(get_db)) -> UserModel:
        user_roles_in_the_division = db.query(RoleModel) \
            .join(UserRoleModel, UserRoleModel.role_id == RoleModel.id) \
            .join(UserModel, UserRoleModel.user_id == UserModel.id) \
            .filter(RoleModel.division == division, UserModel.id == user.id) \
            .all()
        if user_roles_in_the_division:
            for role in user_roles_in_the_division:
                if role.permissions & permission_to_check:
                    return user
                else:
                    continue
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not have permission")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not have role in this division")

    @staticmethod
    def check_special_user_permission(permission_to_check: int, user: UserModel, division: DivisionModel,
                                      db: Session = Depends(get_db)) -> UserModel:
        user_division_permission = db.query(UserDivisionPermissionModel) \
            .filter_by(user_id=user.id, division_id=division.id) \
            .first()
        if user_division_permission and user_division_permission.permissions & permission_to_check:
            return user
        else:
            return None
