import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from api.db.models.base import Base


class SubmissionModel(Base):
    __tablename__ = "submission"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"))
    attachment: Mapped[str] = mapped_column(String, nullable=True)
    note: Mapped[str] = mapped_column(String)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())

    # Many-to-One relationships
    creator: Mapped["UserModel"] = Relationship("UserModel", back_populates="submissions")
    assignment: Mapped["AssignmentModel"] = Relationship("AssignmentModel", back_populates="submissions")
    feedback: Mapped["FeedbackModel"] = Relationship("FeedbackModel", back_populates="submission")

    def __repr__(self):
        return f"""Permission(
                "id": {self.id},
                "creator_id": {self.creator_id},
                "assignment_id": {self.assignment_id},
                "note": {self.note},
                "attachment": {self.attachment},
            )"""