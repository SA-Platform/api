from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, Mapper, DeclarativeBase
from abc import ABC
from starlette import status
from api.db.models import (UserModel,
                           DivisionModel,
                           AssignmentModel,
                           MeetingModel,
                           AnnouncementModel,
                           ExcuseModel)

from api.validators import (UserValidator,
                            AssignmentValidator,
                            DivisionValidator,
                            AnnouncementValidator,
                            MeetingValidator,
                            ExcuseValidator)


class CoreBase(ABC):
    """Base class for all core entities, contains the basic CRUD operations"""
    name: str
    validator: BaseModel
    db_model: DeclarativeBase

    @classmethod
    def get_db_first(cls, db: Session, attribute: str, value: Any):
        return db.query(cls.db_model).filter_by(**{attribute: value}).first()

    @classmethod
    def get_db_range(cls, db: Session, attribute: str, value: Any, limit: int):
        return db.query(cls.db_model).filter_by(**{attribute: value}).limit(limit)

    @classmethod
    def get_db_all(cls, db: Session, attribute: str, value: Any):
        return db.query(cls.db_model).filter_by(**{attribute: value}).all()

    @classmethod
    def get_db_dump(cls, db: Session):
        return db.query(cls.db_model).all()

    @classmethod
    def create(cls, request: BaseModel, db: Session, **kwargs) -> Mapper:
        new_model = cls.db_model(**request.model_dump(), **kwargs)
        db.add(new_model)
        db.commit()
        db.refresh(new_model)
        return new_model

    @classmethod
    def update(cls, model_id: int, request: BaseModel, db: Session, **kwargs) -> Mapper:
        model = cls.get_db_first(db, "id", model_id)
        if model:
            cls.db_update(model, **request.model_dump(), **kwargs)
            db.commit()
            db.refresh(model)
            return model
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__.lower()} not found")

    @classmethod
    def delete(cls, model_id: int, db: Session, user: UserModel | None = None) -> dict:
        model = cls.get_db_first(db, "id", model_id)
        if model:
            db.delete(model)
            db.commit()
            return {"msg": f"{cls.__name__.lower()} deleted"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__.lower()} not found")

    @classmethod
    def db_update(cls, model_instance, **kwargs):
        """this method is used to update a model instance without committing to the database"""
        for key, value in kwargs.items():
            setattr(model_instance, key, value)


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


class Division(CoreBase):
    validator = DivisionValidator
    db_model = DivisionModel

    @classmethod
    def check_division_validity(cls, request: DivisionValidator, db: Session, division_id: int = None) -> None:
        division = cls.get_db_first(db, "name", request.name)
        parent = cls.get_db_first(db, "name", request.parent)
        if request.name == request.parent:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="division can't be its own parent")
        elif request.parent:
            if not parent:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="parent division doesn't exist")
            elif division:
                if division.parent == parent:
                    raise HTTPException(status.HTTP_409_CONFLICT,
                                        detail=f"division {division.name} with the same parent ({parent.name}) already exists")
                elif not division.parent:
                    raise HTTPException(status.HTTP_409_CONFLICT,
                                        detail=f"division {division.name} is a root division and can't have a parent")
        else:
            if division:
                raise HTTPException(status.HTTP_409_CONFLICT, detail=f"division {division.name} already exists")
            else:
                root = db.query(DivisionModel).filter_by(parent=None).first()
                if root:
                    if root.id != division_id:
                        raise HTTPException(status.HTTP_409_CONFLICT,
                                            detail=f"only one root division is allowed, which is {root.name}")


class Assignment(FeatureBase):
    validator = AssignmentValidator
    db_model = AssignmentModel


class Meeting(FeatureBase):
    validator = MeetingValidator
    db_model = MeetingModel


class Announcement(FeatureBase):
    validator = AnnouncementValidator
    db_model = AnnouncementModel


class Excuse(FeatureBase):
    validator = ExcuseValidator
    db_model = ExcuseModel
