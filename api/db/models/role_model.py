from typing import List
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.db.models.base import Base


class RoleModel(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    permissions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user_role_division: Mapped[List["UserRoleDivisionModel"]] = Relationship("UserRoleDivisionModel",
                                                                             back_populates="role",
                                                                             cascade="all, delete")

    def __repr__(self):
        return f"""Role(
            "id": {self.id}
            "name": {self.name}
            "permissions": {self.permissions}
        )"""
