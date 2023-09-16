from typing import TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, Mapper
from starlette import status

from ..core.core_base import CoreBase
from ...db.models import UserModel

T = TypeVar("T")


class SubFeatureBase(CoreBase):
    """Base class for all sub-feature entities, contains the basic CRUD inherited from CoreBase"""

    @classmethod
    def create(cls, request: BaseModel, db: Session, user: UserModel, feature_to_check: str,
               feature_model: T) -> Mapper:
        feature: T | None = db.query(feature_model).filter_by(id=getattr(request, feature_to_check)).first()
        setattr(request, feature_to_check, feature)
        if getattr(request, feature_to_check):
            return super().create(db, creator=user, **request.model_dump(), division=feature.division)
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{feature_to_check} not found")
