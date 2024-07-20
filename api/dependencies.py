from typing import Any

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api.db import SessionLocal
from api.db.models.user_model import UserModel
from api.db.models.division_model import DivisionModel
from api.db.models.role_model import RoleModel
from api.db.models.user_division_permission import UserDivisionPermissionModel
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
            if not db.query(RoleModel).first() or not db.query(
                    DivisionModel).first():  # check if there is any role in the database
                return user

            division: DivisionModel | None = db.query(DivisionModel).filter_by(parent=None).first()
            return self._compare_permissions(user, self.permission_to_check, division, db)

    @classmethod
    async def _read_value_from_request(cls, request: Request, key: str) -> Any:
        return (await request.json())[key]

    @classmethod
    def _compare_permissions(cls, user: UserModel,
                             permission_to_check: int,
                             division: DivisionModel,
                             db: Session) -> UserModel:
        if division:
            user_permissions: UserDivisionPermissionModel | None = db.query(UserDivisionPermissionModel).filter_by(
                user=user,
                division=division).first()
            if user_permissions:
                if (user_permissions.permissions & permission_to_check) == permission_to_check:
                    return user
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"this user does not have the permission to do this action in {division.name} division")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the division this request is sent to does not exist")
