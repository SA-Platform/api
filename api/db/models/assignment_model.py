import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.db.models.base import Base

if TYPE_CHECKING:
    from api.db.models.division_model import DivisionModel
    from api.db.models.excuse_model import ExcuseModel
    from api.db.models.submission_model import SubmissionModel
    from api.db.models.user_model import UserModel


class AssignmentModel(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    date_created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now()
    )
    deadline: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    attachment: Mapped[str | None] = mapped_column(String, nullable=True)
    weight: Mapped[int] = mapped_column(Integer)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"))

    # Many-to-One relationships
    creator: Mapped["UserModel"] = Relationship(
        "UserModel", back_populates="assignments"
    )
    division: Mapped["DivisionModel"] = Relationship(
        "DivisionModel", back_populates="assignments"
    )

    # One-to-Many relationships
    submissions: Mapped[List["SubmissionModel"]] = Relationship(
        "SubmissionModel", back_populates="assignment", cascade="all, delete-orphan"
    )
    excuses: Mapped[List["ExcuseModel"]] = Relationship(
        "ExcuseModel", back_populates="assignment", cascade="all, delete-orphan"
    )

    def update(
        self,
        title: str,
        description: str,
        deadline: DateTime,
        weight: int,
        division: "DivisionModel",
        attachment: str | None = None,
    ) -> None:
        self.title = title
        self.description = description
        self.deadline = deadline
        self.attachment = attachment
        self.weight = weight
        self.division = division

    def __repr__(self):
        return f"""Assignment(
                "id": {self.id},
                "creator_id": {self.creator_id},
                "division_id": {self.division_id},
                "date_created": {self.date_created},
                "title": {self.title},
                "description": {self.description},
                "deadline": {self.deadline},
                "attachment": {self.attachment},
                "weight": {self.weight},
            )"""
