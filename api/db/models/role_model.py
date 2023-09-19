from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.db.models.base import Base


class RoleModel(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"))
    permissions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    division: Mapped["DivisionModel"] = Relationship("DivisionModel", back_populates="roles")

    # user_role_division: Mapped[List["UserRoleDivisionModel"]] = Relationship("UserRoleDivisionModel",
    #                                                                          back_populates="role",
    #                                                                          cascade="all, delete")

    user_role: Mapped[List["UserRoleModel"]] = Relationship("UserRoleModel", back_populates="role",
                                                            cascade="all, delete-orphan")

    def __repr__(self):
        return f"""Role(
            "id": {self.id}
            "name": {self.name}
            "permissions": {self.permissions}
        )"""
