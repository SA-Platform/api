from abc import ABC
from typing import TypeVar, List, Callable

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, Query
from starlette import status

from ...const import CorePermissions, FeaturePermissions
from ...db.models import UserModel

T = TypeVar("T")


class CoreBase(ABC):
    """Base class for all crud entities, contains the basic CRUD operations"""
    db_model: T

    @classmethod
    def get_db_first(cls, db: Session, attribute: str, value: int | str | None) -> T | None:
        return db.query(cls.db_model).filter_by(**{attribute: value}).first()

    @classmethod
    def get_db_range(cls, db: Session, attribute: str, value: int | str, limit: int) -> Query[T]:
        return db.query(cls.db_model).filter_by(**{attribute: value}).limit(limit)

    @classmethod
    def get_db_all(cls, db: Session, attribute: str, value: int | str) -> List[T]:
        return db.query(cls.db_model).filter_by(**{attribute: value}).all()

    @classmethod
    def get_db_dump(cls, db: Session) -> List[T]:
        return db.query(cls.db_model).all()

    # Function to filter the table based on keyword arguments
    @classmethod
    def filter_table(cls, db: Session, **kwargs) -> T | None:

        query = db.query(cls.db_model)

        for attr, value in kwargs.items():
            query = query.filter(getattr(cls.db_model, attr) == value)

        try:
            results = query.first()
            return results
        except NoResultFound:
            return []

    @classmethod
    def filter_all(cls, db: Session, **kwargs) -> List[T]:
        query = db.query(cls.db_model)

        for attr, value in kwargs.items():
            query = query.filter(getattr(cls.db_model, attr) == value)

        try:
            results = query.all()
            return results
        except NoResultFound:
            return []

    @classmethod
    def create(cls, db: Session, **kwargs) -> T:
        new_model = cls.db_model(**kwargs)
        db.add(new_model)
        db.commit()
        db.refresh(new_model)
        return new_model

    @classmethod
    def update(cls, model_id: int, db: Session, **kwargs) -> T:
        model = cls.get_db_first(db, "id", model_id)
        if model:
            cls.db_update(model, **kwargs)
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
    def db_update(cls, model_instance, **kwargs) -> None:
        """this method is used to update a model instance without committing to the database"""
        for key, value in kwargs.items():
            setattr(model_instance, key, value)

    @classmethod
    def _calculate_core_permission(cls, request_permissions: dict) -> int:
        total_request: int = 0
        for permission in CorePermissions:
            if request_permissions[permission.name]:
                total_request = total_request | permission.value
        return total_request

    @classmethod
    def _calculate_feature_permission(cls, request_permissions: dict) -> int:
        total_request: int = 0
        for permission in FeaturePermissions:
            if request_permissions[permission.name]:
                total_request = total_request | permission.value
        return total_request
