import datetime
from typing import List, TYPE_CHECKING

import bcrypt
from sqlalchemy import Integer, DateTime, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.db.models.base import Base

if TYPE_CHECKING:
    from api.db.models.announcement_model import AnnouncementModel
    from api.db.models.assignment_model import AssignmentModel
    from api.db.models.excuse_model import ExcuseModel
    from api.db.models.feedback_model import FeedbackModel
    from api.db.models.meeting_model import MeetingModel
    from api.db.models.submission_model import SubmissionModel
    from api.db.models.user_division_permission import UserDivisionPermissionModel
    from api.db.models.user_role_division import UserRoleDivisionModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    birthdate: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    faculty: Mapped[str] = mapped_column(String)
    university: Mapped[str] = mapped_column(String)
    faculty_department: Mapped[str] = mapped_column(String)
    graduation_year: Mapped[int] = mapped_column(Integer)
    image_file: Mapped[str | None] = mapped_column(String, nullable=True)
    bio: Mapped[str | None] = mapped_column(String, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    date_created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.now()
    )
    permissions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # One-to-Many relationships
    announcements: Mapped[List["AnnouncementModel"]] = Relationship(
        "AnnouncementModel", back_populates="creator", cascade="all, delete-orphan"
    )
    meetings: Mapped[List["MeetingModel"]] = Relationship(
        "MeetingModel", back_populates="creator", cascade="all, delete-orphan"
    )
    assignments: Mapped[List["AssignmentModel"]] = Relationship(
        "AssignmentModel", back_populates="creator", cascade="all, delete-orphan"
    )
    excuses: Mapped[List["ExcuseModel"]] = Relationship(
        "ExcuseModel", back_populates="creator", cascade="all, delete-orphan"
    )
    submissions: Mapped[List["SubmissionModel"]] = Relationship(
        "SubmissionModel", back_populates="creator", cascade="all, delete-orphan"
    )
    feedback: Mapped[List["FeedbackModel"]] = Relationship(
        "FeedbackModel", back_populates="creator", cascade="all, delete-orphan"
    )
    user_role_division: Mapped[List["UserRoleDivisionModel"]] = Relationship(
        "UserRoleDivisionModel", back_populates="user", cascade="all, delete-orphan"
    )
    user_division_permission: Mapped[List["UserDivisionPermissionModel"]] = (
        Relationship(
            "UserDivisionPermissionModel",
            back_populates="user",
            cascade="all, delete-orphan",
        )
    )

    def set_password(self, password) -> str:
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        return self.password

    def check_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def __init__(
        self,
        first_name: str,
        last_name: str,
        birthdate: DateTime,
        phone_number: str,
        email: str,
        username: str,
        password: str,
        faculty: str,
        university: str,
        faculty_department: str,
        graduation_year: int,
        image_file: str | None = None,
        bio: str | None = None,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.phone_number = phone_number
        self.email = email
        self.username = username
        self.set_password(password)
        self.faculty = faculty
        self.university = university
        self.faculty_department = faculty_department
        self.graduation_year = graduation_year
        self.image_file = image_file
        self.bio = bio

    def __repr__(self):
        return f"""User(
            "id": {self.id}
            "first_name": {self.first_name}
            "last_name": {self.last_name}
            "birthday": {self.birthdate}
            "phone_number": {self.phone_number}
            "email": {self.email}
            "faculty": {self.faculty}
            "university": {self.university}
            "faculty_department": {self.faculty_department}
            "graduation_year": {self.graduation_year}
            "image_file": {self.image_file}
            "bio": {self.bio}
            "confirmed": {self.confirmed}
            "username": {self.username}
            "date_created": {self.date_created}
            "password": {self.password}
        )"""
