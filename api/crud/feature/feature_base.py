from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, Mapper
from starlette import status

from ..core.core_base import CoreBase
from ...db.models import UserModel, DivisionModel


class FeatureBase(CoreBase):
    """Base class for all feature entities, contains the basic CRUD inherited from CoreBase"""

    @classmethod
    def create(cls, request: BaseModel, db: Session, user: UserModel, division_id: int) -> Mapper | None:
        division = db.query(DivisionModel).filter_by(id=division_id).first()
        if division:
            return super().create(db, creator=user, division_id=division.id, **request.model_dump())
        raise HTTPException(status.HTTP_404_NOT_FOUND, "division not found")

    @classmethod
    def update(cls, model_id: int, request: BaseModel, db: Session, division_id: int, user: UserModel | None = None,
               **kwargs) -> dict[str: str]:
        model = db.query(cls.db_model).filter_by(id=model_id).first()
        if model:
            division = db.query(DivisionModel).filter_by(id=division_id).first()
            if division:
                super().update(model_id, db, **request.model_dump(), division_id=division.id)
                return model
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="division not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__.lower()} not found")

