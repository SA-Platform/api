import datetime

from sqlalchemy import String, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.db.models.base import Base
from api.db.models.division_model import DivisionModel
from api.db.models.user_model import UserModel


class MeetingModel(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(100))
    date_created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now()
    )
    date: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    location_text: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    location_long: Mapped[float | None] = mapped_column(Float, nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    division_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"))

    # Many-to-One relationships
    division: Mapped["DivisionModel"] = Relationship(
        "DivisionModel", back_populates="meetings"
    )
    creator: Mapped["UserModel"] = Relationship("UserModel", back_populates="meetings")

    def update(
        self,
        title: str,
        description: str,
        date: DateTime,
        location_text: str | None,
        location_lat: float | None,
        location_long: float | None,
        division: "DivisionModel",
    ) -> None:
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
