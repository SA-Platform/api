from .base import Base
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Relationship, mapped_column, Mapped

class UserRoleDivisionPermissionModel(Base):
    __tablename__ = "user_role_division_permission"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), primary_key=True, nullable=True)
    division_id: Mapped[int] = mapped_column(Integer, ForeignKey("divisions.id"), primary_key=True)
    permissions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped["UserModel"] = Relationship("UserModel", back_populates="user_role_division_permission")
    role: Mapped["RoleModel"] = Relationship("RoleModel", back_populates="user_role_division_permission")
    division: Mapped["DivisionModel"] = Relationship("DivisionModel", back_populates="user_role_division_permission")

    def __repr__(self):
        return f"<UserRoleDivisionPermissionModel(user_id={self.user_id}, role_id={self.role_id}, division_id={self.division_id}, permission={self.permissions})>"