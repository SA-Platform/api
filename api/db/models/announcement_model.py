import datetime

from sqlalchemy import String, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.const import AnnouncementsCategory
from api.db.models.base import Base


class AnnouncementModel(Base):
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
    division: Mapped["DivisionModel"] = Relationship("DivisionModel", back_populates="announcements")
    creator: Mapped["UserModel"] = Relationship("UserModel", back_populates="announcements")

    def update(self, title: str, description: str, category: AnnouncementsCategory, date: datetime,
               division: "DivisionModel") -> None:
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