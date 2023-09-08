from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .core_base import CoreBase
from ...db.models import UserModel
from ...validators import UserValidator


class User(CoreBase):
    validator = UserValidator
    db_model = UserModel

    @classmethod
    def get_db_username_or_email(cls, db: Session, username: str):
        return db.query(cls.db_model).filter(
            (cls.db_model.email == username) | (cls.db_model.username == username)).first()

    @classmethod
    def validate_username(cls, db: Session, username: str):
        existing_user = cls.get_db_first(db, "username", username)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username is taken")