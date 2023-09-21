from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .core_base import CoreBase
from .role import Role
from .userrole import UserRole
from ...db.models import UserModel


class User(CoreBase):
    db_model = UserModel

    @classmethod
    def get_db_username_or_email(cls, db: Session, username: str) -> UserModel | None:
        return db.query(cls.db_model).filter(
            (cls.db_model.email == username) | (cls.db_model.username == username)).first()

    @classmethod
    def validate_username(cls, db: Session, username: str) -> None:
        existing_user = cls.get_db_first(db, "username", username)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username is taken")

    @classmethod
    def edit_user_permissions(cls, db: Session, user_id: int, **kwargs) -> None:
        user = cls.get_db_first(db, "id", user_id)
        if user:
            user.permissions = cls._calculate_core_permission(kwargs)
            db.commit()
            db.refresh(user)
            return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    @classmethod
    def assign_user_role(cls, db: Session, user_id: int, role_id: int) -> UserRole:
        user = cls.get_db_first(db, "id", user_id)
        if user:
            role = Role.get_db_first(db, "id", role_id)
            if role:
                if UserRole.filter_table(db, user_id=user_id, role_id=role_id):
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already has this role")
                return UserRole.create(db=db, user_id=user_id, role_id=role_id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="role not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
