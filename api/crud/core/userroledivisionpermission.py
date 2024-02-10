from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .core_base import CoreBase
from .division import Division
from .role import Role
from .user import User
from ...db.models import UserModel, DivisionModel, RoleModel, \
    UserRoleDivisionPermissionModel


class UserRoleDivisionPermission(CoreBase):
    db_model = UserRoleDivisionPermissionModel

    @classmethod
    def create(cls, db: Session, user_id: int, division_id: int, role_id: int,
               **kwargs) -> UserRoleDivisionPermissionModel:
        user = User.get_db_first(db, "id", user_id)
        division = Division.get_db_first(db, "id", division_id)

        if cls.filter_table(db, user_id=user_id, division_id=division_id, role_id=role_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="User already in this and have the same role")

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if not division:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Division not found")

        return super().create(
            db, user_id=user_id, division_id=division_id, role_id=role_id,
            permissions=cls._calculate_feature_permission(kwargs)
        )

    @classmethod
    def delete(cls, db: Session, user_id: int, division_id: int, role_id: int | None, ) -> dict:
        record = db.query(cls.db_model).filter(
            (cls.db_model.user_id == user_id) &
            (cls.db_model.division_id == division_id)
            & (cls.db_model.role_id == role_id)
        ).first()
        if record:
            db.delete(record)
            db.commit()

            return {"message": "record deleted successfully"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="record not found")
