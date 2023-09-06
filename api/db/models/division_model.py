from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.db.models.base import Base


class DivisionModel(Base):
    __tablename__ = "divisions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    parent_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"), nullable=True)

    # One-to-Many relationships
    subdivisions: Mapped[List["DivisionModel"]] = Relationship("DivisionModel", back_populates="parent",
                                                               cascade="all, delete")
    parent: Mapped["DivisionModel"] = Relationship("DivisionModel", back_populates="subdivisions", remote_side=[id])
    announcements: Mapped[List["AnnouncementModel"]] = Relationship("AnnouncementModel", back_populates="division",
                                                                    cascade="all, delete")
    meetings: Mapped[List["MeetingModel"]] = Relationship("MeetingModel", back_populates="division",
                                                          cascade="all, delete")
    assignments: Mapped[List["AssignmentModel"]] = Relationship("AssignmentModel", back_populates="division",
                                                                cascade="all, delete")

    def __repr__(self):
        return f"""(id: {self.id}, name: {self.name}, parent: {self.parent})"""
