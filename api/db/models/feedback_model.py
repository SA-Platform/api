import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from api.db.models.base import Base

if TYPE_CHECKING:
    from api.db.models.division_model import DivisionModel
    from api.db.models.submission_model import SubmissionModel
    from api.db.models.user_model import UserModel


class FeedbackModel(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    submission_id: Mapped[int] = mapped_column(ForeignKey("submission.id"))
    attachment: Mapped[str] = mapped_column(String, nullable=True)
    score: Mapped[int] = mapped_column(Integer)  #############
    note: Mapped[str] = mapped_column(String)
    date_created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now()
    )
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"))

    # Many-to-One relationships
    creator: Mapped["UserModel"] = Relationship("UserModel", back_populates="feedback")
    submission: Mapped["SubmissionModel"] = Relationship(
        "SubmissionModel", back_populates="feedback"
    )
    division: Mapped["DivisionModel"] = Relationship(
        "DivisionModel", back_populates="feedback"
    )

    def __repr__(self):
        return f"""Permission(
                "id": {self.id},
                "creator_id": {self.creator_id},
                "submission_id": {self.submission_id},
                "attachment": {self.attachment},
                "score": {self.score},
                "note": {self.note},
            )"""
