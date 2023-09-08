from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, Mapper
from starlette import status

from ..core.core_base import CoreBase
from ...db.models import UserModel, DivisionModel


class FeatureBase(CoreBase):
    """Base class for all feature entities, contains the basic CRUD crud inherited from CoreBase"""

    @classmethod
    def create(cls, request: BaseModel, db: Session, user: UserModel) -> Mapper:
        request.division = db.query(DivisionModel).filter_by(name=request.division).first()
        if request.division:
            return super().create(db, creator=user, **request.model_dump())
        raise HTTPException(status.HTTP_404_NOT_FOUND, "division not found")

    @classmethod
    def update(cls, model_id: int, request: BaseModel, db: Session, user: UserModel | None = None, **kwargs) -> dict:
        model = db.query(cls.db_model).filter_by(id=model_id).first()
        if model:
            request.division = db.query(DivisionModel).filter_by(name=request.division).first()
            if request.division:
                cls.db_update(model, **request.model_dump())
                db.commit()
                return {"msg": "updates saved"}
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="division not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__.lower()} not found")
