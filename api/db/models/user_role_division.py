from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Relationship, mapped_column, Mapped


class UserRoleDivisionModel(Base):
    __tablename__ = "user_role_division"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"), primary_key=True)

    user: Mapped["UserModel"] = Relationship("UserModel", back_populates="user_role_division")
    role: Mapped["RoleModel"] = Relationship("RoleModel", back_populates="user_role_division")
    division: Mapped["DivisionModel"] = Relationship("DivisionModel", back_populates="user_role_division")

    def __repr__(self):
        return f"<UserRoleDivisionModel(user_id={self.user_id}, role_id={self.role_id}, division_id={self.division_id})>"
