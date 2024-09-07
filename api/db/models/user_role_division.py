from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Relationship, mapped_column, Mapped

if TYPE_CHECKING:
    from api.db.models.division_model import DivisionModel
    from api.db.models.role_model import RoleModel
    from api.db.models.user_model import UserModel


from .base import Base


class UserRoleDivisionModel(Base):
    __tablename__ = "user_role_division"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    division_id: Mapped[int] = mapped_column(
        ForeignKey("divisions.id"), primary_key=True
    )

    user: Mapped["UserModel"] = Relationship(
        "UserModel", back_populates="user_role_division"
    )
    role: Mapped["RoleModel"] = Relationship(
        "RoleModel", back_populates="user_role_division"
    )
    division: Mapped["DivisionModel"] = Relationship(
        "DivisionModel", back_populates="user_role_division"
    )

    def __repr__(self):
        return f"<UserRoleDivisionModel(user_id={self.user_id}, role_id={self.role_id}, division_id={self.division_id})>"
