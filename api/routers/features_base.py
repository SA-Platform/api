from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, Mapper, DeclarativeBase
from abc import ABC
from typing import Optional
from starlette import status

from api.db.models.core_models import UserModel, DivisionModel
from api.db.models.feature_models import AssignmentModel, MeetingModel, AnnouncementModel
from api.validators import UserValidator, AssignmentValidator


class Base(ABC):
    """Base class for all features, contains the basic CRUD operations"""
    name: str
    tag: str
    path: str
    router: APIRouter
    validator: BaseModel
    db_model: DeclarativeBase

    @classmethod
    def get_db_first(cls, db: Session, attribute: str, value: str):
        return db.query(cls.db_model).filter_by(**{attribute: value}).first()

    @classmethod
    def get_db_range(cls, db: Session, attribute: str, value: str, limit: int):
        return db.query(cls.db_model).filter_by(**{attribute: value}).limit(limit)

    @classmethod
    def get_db_all(cls, db: Session, attribute: str, value: str):
        return db.query(cls.db_model).filter_by(**{attribute: value}).all()

    @classmethod
    def get_db_dump(cls, db: Session):
        return db.query(cls.db_model).all()

    @classmethod
    def create(cls, request: BaseModel, db: Session, user: UserModel | None = None) -> Mapper:
        new_model = cls.db_model(**request.model_dump())
        db.add(new_model)
        db.commit()
        return new_model

    @classmethod
    def update(cls, request: BaseModel, db: Session, user: UserModel | None) -> Mapper:
        model = cls.get_db_first(db, "id", request.id)
        if model:
            model.update(**request.model_dump(exclude={"id"}))
            db.commit()
            db.refresh(model)
            return model
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.name} not found")

    @classmethod
    def delete(cls, model_id: int, db: Session, user: UserModel | None = None) -> dict:
        model = cls.get_db_first(db, "id", model_id)
        if model:
            db.delete(model)
            db.commit()
            return {"msg": f"{cls.name} deleted"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.name} not found")


class FeatureBase(Base):

    @classmethod
    def create(cls, request: BaseModel, db: Session, user: UserModel) -> dict:
        request.division = db.query(DivisionModel).filter_by(name=request.division).first()
        if request.division:
            new_model = cls.db_model(**request.model_dump(), creator=user)
            db.add(new_model)
            db.commit()
            return {"msg": f"{cls.name} created"}
        raise HTTPException(status.HTTP_404_NOT_FOUND, "division not found")

    @classmethod
    def update(cls, request: BaseModel, db: Session, user: UserModel | None = None) -> dict:
        model = db.query(cls.db_model).filter_by(id=request.id).first()
        if model:
            request.division = db.query(DivisionModel).filter_by(name=request.division).first()
            if request.division:
                model.update(**request.model_dump(exclude={"id"}))
                db.commit()
                return {"msg": "updates saved"}
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="division not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.name} not found")


class User(Base):
    name = "User"
    tag = "Users"
    path = "/users"
    router = APIRouter(tags=[tag])
    validator = UserValidator
    db_model = UserModel

    @classmethod
    def get_db_username_or_email(cls, db: Session, username: str):
        return db.query(cls.db_model).filter((cls.db_model.email == username) | (cls.db_model.username == username)).first()


class Assignment(FeatureBase):
    name = "Assignment"
    tag = "Assignments"
    path = "/assignments"
    router = APIRouter(tags=[tag])
    validator = AssignmentValidator
    db_model = AssignmentModel


class Meeting(FeatureBase):
    name = "Meeting"
    tag = "Meetings"
    path = "/meetings"
    router = APIRouter(tags=[tag])
    validator = UserValidator
    db_model = MeetingModel


class Announcement(FeatureBase):
    name = "Announcement"
    tag = "Announcements"
    path = "/announcements"
    router = APIRouter(tags=[tag])
    validator = UserValidator
    db_model = AnnouncementModel

