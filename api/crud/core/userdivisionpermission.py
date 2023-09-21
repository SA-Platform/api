from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .core_base import CoreBase
from .division import Division
from .user import User
from ...db.models import UserModel, DivisionModel, UserDivisionPermissionModel, RoleModel


class UserDivisionPermission(CoreBase):
    db_model = UserDivisionPermissionModel

    @classmethod
    def create(cls, db: Session, user_id: int, division_id: int, **kwargs) -> UserDivisionPermissionModel:
        user = User.get_db_first(db, "id", user_id)
        division = Division.get_db_first(db, "id", division_id)

        if cls.filter_table(db, user_id=user_id, division_id=division_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already in this division")

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if not division:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Division not found")

        return super().create(
            db, user_id=user_id, division_id=division_id,
            permissions=cls._calculate_feature_permission(kwargs)
        )

    @classmethod
    def delete(cls, db: Session, user_id: int, division_id: int) -> dict:
        record = db.query(cls.db_model).filter(
            (cls.db_model.user_id == user_id) &
            (cls.db_model.division_id == division_id)
        ).first()
        if record:
            db.delete(record)
            db.commit()

            return {"message": "record deleted successfully"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="record not found")



