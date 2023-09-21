from typing import TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, Mapper

from ..core.core_base import CoreBase
from ..feature.feature_base import FeatureBase
from ...db.models import UserModel
from ...db.models.division_model import DivisionModel

T = TypeVar("T")


class SubFeatureBase(CoreBase):
    """Base class for all sub-feature entities, contains the basic CRUD inherited from CoreBase"""
    parent_name: str
    parent_model: T

    @classmethod
    def create(cls, request: BaseModel, db: Session, user: UserModel, feature_to_check: str,
               feature_model: T) -> Mapper:
        feature: T | None = db.query(feature_model).filter_by(id=getattr(request, feature_to_check)).first()
        setattr(request, feature_to_check, feature)
        if getattr(request, feature_to_check):
            return super().create(db, creator=user, **request.model_dump(), division=feature.division)
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{feature_to_check} not found")

    @classmethod
    def update(cls, model_id: int, request: BaseModel, db: Session, division_id: int, user: UserModel | None = None,
               **kwargs) -> dict[str: str]:
        model = db.query(cls.db_model).filter_by(id=model_id).first()
        if model:
            division = db.query(DivisionModel).filter_by(id=division_id).first()
            if division:
                super().update(model_id, db, **request.model_dump())
                return model
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="division not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__.lower()} not found")
