import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.const import AnnouncementsCategory
from api.db.models.base import Base

if TYPE_CHECKING:
    from api.db.models.core_models import User, Division
    from api.db.models.sub_models import Submission, Excuse


class Assignment(Base):
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
    creator: Mapped["User"] = Relationship("User", back_populates="assignments")
    division: Mapped["Division"] = Relationship("Division", back_populates="assignments")

    # One-to-Many relationships
    submissions: Mapped["Submission"] = Relationship("Submission", back_populates="assignment")
    excuses: Mapped["Excuse"] = Relationship("Excuse", back_populates="assignment")

    def update(self, title: str, description: str, deadline: datetime,
               weight: int, division: "Division", attachment: str | None = None) -> None:
        self.title = title
        self.description = description
        self.deadline = deadline
        self.attachment = attachment
        self.weight = weight
        self.division = division

    def __repr__(self):
        return f"""Permission(
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


class Announcement(Base):
    __tablename__ = "announcements"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    category: Mapped[AnnouncementsCategory] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"))

    # One-to-Many relationships
    division: Mapped["Division"] = Relationship("Division", back_populates="announcements")
    creator: Mapped["User"] = Relationship("User", back_populates="announcements")

    def update(self, title: str, description: str, category: AnnouncementsCategory, date: datetime,
               division: "Division") -> None:
        self.title = title
        self.description = description
        self.category = category
        self.date = date
        self.division = division

    def __repr__(self):
        return f"""Permission(
                "id": {self.id},
                "creator_id": {self.creator_id},
                "division_id": {self.division_id},
                "date_created": {self.date_created},
                "date": {self.date},
                "category": {self.category},
                "title": {self.title},
                "description": {self.description},
            )"""


class Meeting(Base):
    __tablename__ = 'meetings'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(100))
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    location_text: Mapped[str] = mapped_column(String(100), nullable=True)
    location_lat: Mapped[float] = mapped_column(Float, nullable=True)
    location_long: Mapped[float] = mapped_column(Float, nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"))

    # Many-to-One relationships
    division: Mapped["Division"] = Relationship("Division", back_populates="meetings")
    creator: Mapped["User"] = Relationship("User", back_populates="meetings")

    def update(self, title: str, description: str, date: datetime, location_text: str | None,
               location_lat: float | None, location_long: float | None, division: "Division") -> None:
        self.title = title
        self.description = description
        self.date = date
        self.location_text = location_text
        self.location_lat = location_lat
        self.location_long = location_long
        self.division = division

    def repr(self):
        return f"""Meeting(
            "id": {self.id}
            "title": {self.title}
            "description": {self.description}
            "date": {self.date}
            "date_created": {self.date_created}
            "location_text": {self.location_text}
            "location_lat": {self.location_lat}
            "location_long": {self.location_long}
            "creator_id": {self.creator_id}
            "division_id": {self.division_id}
        )"""
