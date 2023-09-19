from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, Mapper
from starlette import status

from ..core.core_base import CoreBase
from ...db.models import UserModel, DivisionModel, UserDivisionPermissionModel


class FeatureBase(CoreBase):
    """Base class for all feature entities, contains the basic CRUD inherited from CoreBase"""

    @classmethod
    def create(cls, request: BaseModel, db: Session, user: UserModel) -> Mapper | None:
        request.division = db.query(DivisionModel).filter_by(name=request.division).first()
        if request.division:
            cls._compare_permissions(user, cls._fetch_permission_value("CREATE"), request.division, db)
            return super().create(db, creator=user, **request.model_dump())
        raise HTTPException(status.HTTP_404_NOT_FOUND, "division not found")

    @classmethod
    def update(cls, model_id: int, request: BaseModel, db: Session, user: UserModel | None = None, **kwargs) -> dict[
                                                                                                                str: str]:
        model = db.query(cls.db_model).filter_by(id=model_id).first()
        if model:
            request.division = db.query(DivisionModel).filter_by(name=request.division).first()
            if request.division:
                cls._compare_permissions(user, cls._fetch_permission_value("UPDATE"), request.division, db)
                cls.db_update(model, **request.model_dump())
                db.commit()
                db.refresh(model)
                return model
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="division not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__.lower()} not found")

    @classmethod
    def delete(cls, model_id: int, db: Session, user: UserModel) -> dict:
        model = cls.get_db_first(db, "id", model_id)
        if model:
            cls._compare_permissions(user, cls._fetch_permission_value("DELETE"), model.division, db)
            db.delete(model)
            db.commit()
            return {"msg": f"{cls.__name__.lower()} deleted"}

    @classmethod
    def _fetch_permission_value(cls, action: str) -> int:
        return getattr(Permissions, f"{action}_{cls.__name__.upper()}")

    @classmethod
    def _compare_permissions(cls, user: UserModel,
                             permission_to_check: int,
                             division: DivisionModel,
                             db: Session) -> UserModel:

        user_permissions: UserDivisionPermissionModel | None = db.query(UserDivisionPermissionModel).filter_by(
            user=user,
            division=division).first()
        if user_permissions:
            if (user_permissions.permissions & permission_to_check) == permission_to_check:
                return user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"this user does not have the permission to do this action in {division.name} division")
