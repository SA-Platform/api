from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Relationship
from typing import TYPE_CHECKING
from api.db.models.base import Base

if TYPE_CHECKING:
    from api.db.models.role_model import RoleModel


class PermissionModel(Base):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(primary_key=True)
    create_task: Mapped[bool]
    create_announcement: Mapped[bool]
    create_meeting: Mapped[bool]
    edit_task: Mapped[bool]
    edit_announcement: Mapped[bool]
    edit_meeting: Mapped[bool]
    respond_to_task: Mapped[bool]
    set_role: Mapped[bool]
    edit_role: Mapped[bool]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    # One-to-One relationships
    role: Mapped["RoleModel"] = Relationship("RoleModel", back_populates="permissions")

    def __repr__(self):
        return f"""Permission(
            "id": {self.id}
            "create_task": {self.create_task}
            "create_announcement": {self.create_announcement}
            "create_meeting": {self.create_meeting}
            "edit_task": {self.edit_task}
            "edit_announcement": {self.edit_announcement}
            "edit_meeting": {self.edit_meeting}
            "respond_to_task": {self.respond_to_task}
            "set_role": {self.set_role}
            "edit_role": {self.edit_role}
            "role_id": {self.role_id}
        )"""
