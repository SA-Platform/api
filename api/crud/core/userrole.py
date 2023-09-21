from sqlalchemy.orm import Session

from api.crud.core.core_base import CoreBase

from ...db.models import UserRoleModel


class UserRole(CoreBase):
    db_model = UserRoleModel

    @classmethod
    def delete(cls, db: Session, user_id: int, role_id: int) -> dict:
        # Use UserRoleModel for database operations
        db.query(cls.db_model).filter_by(user_id=user_id, role_id=role_id).delete()
        db.commit()
        return {"message": "record deleted successfully"}
