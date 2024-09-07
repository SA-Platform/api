from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Relationship, mapped_column, Mapped

from api.db.models.division_model import DivisionModel
from api.db.models.user_model import UserModel

from .base import Base


class UserDivisionPermissionModel(Base):
    __tablename__ = "user_division_permission"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    division_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("divisions.id"), primary_key=True
    )
    permissions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped["UserModel"] = Relationship(
        "UserModel", back_populates="user_division_permission"
    )
    division: Mapped["DivisionModel"] = Relationship(
        "DivisionModel", back_populates="user_division_permission"
    )

    def __repr__(self):
        return f"<UserDivisionPermissionModel(user_id={self.user_id}, division_id={self.division_id}, permission={self.permissions})>"
