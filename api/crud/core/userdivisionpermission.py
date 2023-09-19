from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .core_base import CoreBase
from .division import Division
from .user import User
from ...const import CorePermissions
from ...db.models import UserModel, DivisionModel, UserDivisionPermissionModel, RoleModel
from ...utils import decode_permissions


class UserDivisionPermission(CoreBase):
    db_model = UserDivisionPermissionModel

    @classmethod
    def create(cls, db: Session, user_id: int, division_id: int,
               **kwargs) -> UserDivisionPermissionModel:
        user = User.get_db_first(db, "id", user_id)
        division = Division.get_db_first(db, "id", division_id)
        if cls.get_db_first(db, "user_id", user_id) and cls.get_db_first(db, "division_id", division_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user division permission already exists")
        if user:
            if division:
                return super().create(db, user_id=user_id, division_id=division_id,
                                      permissions=cls._calculate_feature_permission(kwargs.get("permissions")))
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="division not found")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    # @classmethod
    # def create(cls, db: Session, user_id: int, division_id: int, permission: int) -> UserDivisionPermissionModel:
    #     user = User.get_db_first(db, "id", user_id)
    #     if user:
    #         division = Division.get_db_first(db, "id", division_id)
    #         if division:
    #             cls._add_user_division_permission_record(db, user, division)
    #             return super().create(db, user=user, division=division)
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="division not found")
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

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

    # @classmethod
    # def _add_user_division_permission_record(cls, db: Session, user: UserModel,
    #                                          division: DivisionModel) -> UserDivisionPermissionModel:
    #     existing_record = cls.get_db_first(db, "user_id", user.id)
    #     if existing_record and existing_record.division_id == division.id:
    #         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User division permission already exists")
    #
    #     if existing_record is None:
    #         return super().create(db, user_id=user.id, division_id=division.id,
    #                               permissions=0)

        return existing_record

    @classmethod
    def _delete_user_division_permission_record(cls, db: Session, user: UserModel, division: DivisionModel,
                                                role: RoleModel) -> UserDivisionPermissionModel:
        record = db.query(UserDivisionPermissionModel).filter(
            (UserDivisionPermissionModel.user == user) &
            (UserDivisionPermissionModel.division == division)
        ).first()
        if record:
            record.permissions &= ~role.permissions
            if record.permissions == 0:
                db.delete(record)
        return record
