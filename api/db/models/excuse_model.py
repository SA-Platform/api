import datetime

from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from api.db.models.base import Base


class ExcuseModel(Base):
    __tablename__ = "excuse"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"))
    description: Mapped[str] = mapped_column(String)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())
    validity: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    accepted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Many-to-one relationships
    creator: Mapped["UserModel"] = Relationship("UserModel", back_populates="excuses")
    assignment: Mapped["AssignmentModel"] = Relationship("AssignmentModel", back_populates="excuses")

    def update(self, description: str, validity: datetime, accepted: bool) -> None:
        self.description = description
        self.validity = validity
        self.accepted = accepted

    def __repr__(self):
        return f"""Permission(
                "id": {self.id},
                "creator_id": {self.creator_id},
                "assignment_id": {self.assignment_id},
                "description": {self.description},
                "validity": {self.validity},
                "accepted": {self.accepted},
            )"""
