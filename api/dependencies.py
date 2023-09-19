from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

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


# class CheckPermission:
#     def __init__(self, permission_to_check: int, core: bool = False):
#         self.permission_to_check: int = permission_to_check
#         self.core: bool = core
#
#     # async def __call__(self, request: Request,
#     #                    user: UserModel = Depends(get_current_user),
#     #                    db: Session = Depends(get_db)) -> UserModel:
#     #
#     #     if self.core:
#     #         if not self.is_core_data_present(db):
#     #             return user
#     #
#     #         division: DivisionModel | None = self.get_top_level_division(db)
#     #         return self.check_permissions(user, self.permission_to_check, division, db)
#     #
#     # @staticmethod
#     # async def _read_value_from_request(request: Request, key: str) -> Any:
#     #     return (await request.json())[key]
#     #
#     # @staticmethod
#     # def is_core_data_present(db: Session) -> bool:
#     #     return db.query(RoleModel).first() is not None and db.query(DivisionModel).first() is not None
#     #
#     # @staticmethod
#     # def get_top_level_division(db: Session) -> DivisionModel | None:
#     #     return db.query(DivisionModel).filter_by(parent=None).first()
#     #
#     # @staticmethod
#     # def check_permissions(user: UserModel, permission_to_check: int, division: DivisionModel, db: Session)
#     -> UserModel:
#     #     if division:
#     #         user_permissions = db.query(UserDivisionPermissionModel).filter_by(
#     #             user=user,
#     #             division=division
#     #         ).first()
#     #         if user_permissions and (user_permissions.permissions & permission_to_check) == permission_to_check:
#     #             return user
#     #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#     #                             detail=f"User does not have permission in {division.name} division")
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#     #                         detail="The division does not exist")
#     #


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
            # Check role permission
            division: DivisionModel | None = db.query(DivisionModel).filter_by(
                id=request.path_params["division_id"]).first()
            role_user = self.check_role_permission(self.permission_to_check, user, division, db)

            if role_user is not None:
                return role_user
            else:
                # Check special user permission
                special_user = self.check_special_user_permission(self.permission_to_check, user,
                                                                  request.path_params["division_id"], db)
                if special_user is not None:
                    return special_user

    @staticmethod
    def check_user_permission(permission_to_check: int, user: UserModel) -> UserModel:
        if user.permissions & permission_to_check:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not have permission")

    @staticmethod
    def check_role_permission(permission_to_check: int, user: UserModel, division: DivisionModel,
                              db: Session = Depends(get_db)) -> UserModel:
        user_role_within_division = db.query(RoleModel).join(UserRoleModel).join(UserModel).filter(
            UserModel.id == user.id).first()

        if user_role_within_division is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="User does not have permission in this division")
        if user_role_within_division.permissions & permission_to_check:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not have permission")

    @staticmethod
    def check_special_user_permission(permission_to_check: int, user: UserModel, division: DivisionModel,
                                      db: Session = Depends(get_db)) -> UserModel:
        user_division_permission = db.query(UserDivisionPermissionModel).filter(
            UserDivisionPermissionModel.user == user,
            UserDivisionPermissionModel.division == division
        ).first()
        if user_division_permission.permissions & permission_to_check:
            return user
