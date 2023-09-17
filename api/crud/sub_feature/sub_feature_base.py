from typing import TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, Mapper

from ..feature.feature_base import FeatureBase
from ...db.models import UserModel

T = TypeVar("T")


class SubFeatureBase(FeatureBase):
    """Base class for all sub-feature entities, contains the basic CRUD inherited from CoreBase"""
    parent_name: str
    parent_model: T

    @classmethod
    def create(cls, request: BaseModel, db: Session, user: UserModel) -> Mapper:
        parent: T | None = db.query(cls.parent_model).filter_by(id=getattr(request, cls.parent_name)).first()
        if parent:
            setattr(request, cls.parent_name, parent)
            cls._compare_permissions(user, cls._fetch_permission_value("CREATE"), parent.division, db)
            return super(FeatureBase, cls).create(db, creator=user, **request.model_dump(), division=parent.division)
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{cls.parent_name} not found")

    @classmethod
    def update(cls, model_id: int, db: Session, user: UserModel, **kwargs) -> T:
        model = cls.get_db_first(db, "id", model_id)
        if model:
            cls._compare_permissions(user, cls._fetch_permission_value("UPDATE"),
                                     getattr(model, cls.parent_name).division, db)
            cls.db_update(model, **kwargs)
            db.commit()
            db.refresh(model)
            return model
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__.lower()} not found")
