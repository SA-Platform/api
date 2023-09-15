from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, Mapper
from starlette import status

from ..core.core_base import CoreBase
from ...db.models import UserModel


class SubFeatureBase(CoreBase):
    """Base class for all sub-feature entities, contains the basic CRUD inherited from CoreBase"""

    @classmethod
    def create(cls, request: BaseModel, db: Session, user: UserModel, feature_to_check: str,
               feature_model: Mapper) -> Mapper:
        setattr(request, feature_to_check,
                db.query(feature_model).filter_by(id=getattr(request, feature_to_check)).first())
        if getattr(request, feature_to_check):
            return super().create(db, creator=user, **request.model_dump())
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{feature_to_check} not found")
