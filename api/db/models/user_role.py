from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.db.models.base import Base


class UserRoleModel(Base):
    __tablename__ = "user_role"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False, primary_key=True)

    user: Mapped["UserModel"] = Relationship("UserModel", back_populates="user_role")
    role: Mapped["RoleModel"] = Relationship("RoleModel", back_populates="user_role")

    def __repr__(self):
        return f"""UserRole(
            "user_id": {self.user_id}
            "role_id": {self.role_id}
        )"""
