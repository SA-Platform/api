import datetime
from typing import List
from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.db.models.base import Base


class AssignmentModel(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    attachment: Mapped[str] = mapped_column(String, nullable=True)
    weight: Mapped[int] = mapped_column(Integer)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"))

    # Many-to-One relationships
    creator: Mapped["UserModel"] = Relationship("UserModel", back_populates="assignments")
    division: Mapped["DivisionModel"] = Relationship("DivisionModel", back_populates="assignments")

    # One-to-Many relationships
    submissions: Mapped[List["SubmissionModel"]] = Relationship("SubmissionModel", back_populates="assignment")
    excuses: Mapped[List["ExcuseModel"]] = Relationship("ExcuseModel", back_populates="assignment")

    def update(self, title: str, description: str, deadline: datetime,
               weight: int, division: "DivisionModel", attachment: str | None = None) -> None:
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
