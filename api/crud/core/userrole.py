from sqlalchemy.orm import Session

from api.crud.core.core_base import CoreBase

from ...db.models import UserRoleModel


class UserRole(CoreBase):
    db_model = UserRoleModel

