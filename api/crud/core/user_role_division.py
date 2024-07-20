from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .core_base import CoreBase
from .division import Division
from .role import Role
from .user import User
from ...db.models.user_model import UserModel
from ...db.models.division_model import DivisionModel
from ...db.models.role_model import RoleModel
from ...db.models.user_role_division import UserRoleDivisionModel
from ...db.models.user_division_permission import UserDivisionPermissionModel


class UserRoleDivision(CoreBase):
    db_model = UserRoleDivisionModel

    @classmethod
    def create(cls, db: Session, user_id: int, role_id: int, division_id: int) -> UserRoleDivisionModel:
        user = User.get_db_first(db, "id", user_id)
        if user:
            role = Role.get_db_first(db, "id", role_id)
            if role:
                division = Division.get_db_first(db, "id", division_id)
                if division:
                    cls._add_user_division_permission_record(db, user, division, role)
                    return super().create(db, user=user, role=role, division=division)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="division not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="role not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    @classmethod
    def delete(cls, db: Session, user_id: int, role_id: int, division_id: int) -> dict:
        record = db.query(cls.db_model).filter(
            (cls.db_model.user_id == user_id) &
            (cls.db_model.role_id == role_id) &
            (cls.db_model.division_id == division_id)
        ).first()
        if record:
            db.delete(record)
            db.delete(cls._delete_user_division_permission_record(db, record.user, record.division, record.role))
            db.commit()

            return {"message": "record deleted successfully"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="record not found")

    @classmethod
    def _add_user_division_permission_record(cls, db: Session, user: UserModel, division: DivisionModel,
                                             role: RoleModel) -> UserDivisionPermissionModel:
        record = db.query(UserDivisionPermissionModel).filter(
            (UserDivisionPermissionModel.user == user) &
            (UserDivisionPermissionModel.division == division)
        ).first()
        if record:
            record.permissions |= role.permissions
        else:
            record = UserDivisionPermissionModel(user=user, division=division, permissions=role.permissions)
            db.add(record)
        return record

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
