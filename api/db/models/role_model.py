from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.db.models.base import Base

if TYPE_CHECKING:
    from api.db.models.permission_model import PermissionModel


class RoleModel(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    # One-to-One relationships
    permissions: Mapped["PermissionModel"] = Relationship("PermissionModel", back_populates="role")

    def __repr__(self):
        return f"""Role(
            "id": {self.id}
            "name": {self.name}
        )"""
