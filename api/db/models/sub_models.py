import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from api.db.models.base import Base

if TYPE_CHECKING:
    from api.db.models.feature_models import Assignment
    from api.db.models.core_models import User


class Submission(Base):
    __tablename__ = "submission"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"))
    attachment: Mapped[str] = mapped_column(String, nullable=True)
    note: Mapped[str] = mapped_column(String)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())

    # Many-to-One relationships
    creator: Mapped["User"] = Relationship("User", back_populates="submissions")
    assignment: Mapped["Assignment"] = Relationship("Assignment", back_populates="submissions")
    feedback: Mapped["Feedback"] = Relationship("Feedback", back_populates="submission")

    def __repr__(self):
        return f"""Permission(
                "id": {self.id},
                "creator_id": {self.creator_id},
                "assignment_id": {self.assignment_id},
                "note": {self.note},
                "attachment": {self.attachment},
            )"""


class Excuse(Base):
    __tablename__ = "excuse"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"))
    description: Mapped[str] = mapped_column(String)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())
    validity: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    accepted: Mapped[bool] = mapped_column(Boolean)

    # Many-to-one relationships
    creator: Mapped["User"] = Relationship("User", back_populates="excuses")
    assignment: Mapped["Assignment"] = Relationship("Assignment", back_populates="excuses")

    def __repr__(self):
        return f"""Permission(
                "id": {self.id},
                "creator_id": {self.creator_id},
                "assignment_id": {self.assignment_id},
                "description": {self.description},
                "validity": {self.validity},
                "accepted": {self.accepted},
            )"""


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    submission_id: Mapped[int] = mapped_column(ForeignKey("submission.id"))
    attachment: Mapped[str] = mapped_column(String, nullable=True)
    score: Mapped[int] = mapped_column(Integer)  #############
    note: Mapped[str] = mapped_column(String)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())

    # Many-to-One relationships
    creator: Mapped["User"] = Relationship("User", back_populates="feedback")
    submission: Mapped["Submission"] = Relationship("Submission", back_populates="feedback")

    def __repr__(self):
        return f"""Permission(
                "id": {self.id},
                "creator_id": {self.creator_id},
                "submission_id": {self.submission_id},
                "attachment": {self.attachment},
                "score": {self.score},
                "note": {self.note},
            )"""
