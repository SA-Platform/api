import datetime
from typing import List, TYPE_CHECKING

import bcrypt
from sqlalchemy import Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from api.db.models.base import Base

if TYPE_CHECKING:
    from api.db.models.feature_models import Announcement, Meeting, Assignment
    from api.db.models.sub_models import Submission, Excuse, Feedback


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    birthdate: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    faculty: Mapped[str] = mapped_column(String)
    university: Mapped[str] = mapped_column(String)
    faculty_department: Mapped[str] = mapped_column(String)
    graduation_year: Mapped[int] = mapped_column(Integer)
    image_file: Mapped[str] = mapped_column(String, nullable=True)
    bio: Mapped[str] = mapped_column(String, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())

    # One-to-Many relationships
    announcements: Mapped[List["Announcement"]] = Relationship("Announcement", back_populates="creator")
    meetings: Mapped[List["Meeting"]] = Relationship("Meeting", back_populates="creator")
    assignments: Mapped[List["Assignment"]] = Relationship("Assignment", back_populates="creator")
    excuses: Mapped[List["Excuse"]] = Relationship("Excuse", back_populates="creator")
    submissions: Mapped[List["Submission"]] = Relationship("Submission", back_populates="creator")
    feedback: Mapped[List["Feedback"]] = Relationship("Feedback", back_populates="creator")

    def set_password(self, password) -> str:
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        return self.password

    def check_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def __init__(self, first_name: str, last_name: str, birthdate: datetime.datetime,
                 phone_number: str, email: str, username: str, password: str,
                 faculty: str, university: str, faculty_department: str,
                 graduation_year: int, image_file: str | None = None, bio: str | None = None) -> None:
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


class Permission(Base):
    __tablename__ = 'permissions'

    id: Mapped[int] = mapped_column(primary_key=True)
    create_task: Mapped[bool]
    create_announcement: Mapped[bool]
    create_meeting: Mapped[bool]
    edit_task: Mapped[bool]
    edit_announcement: Mapped[bool]
    edit_meeting: Mapped[bool]
    respond_to_task: Mapped[bool]
    set_role: Mapped[bool]
    edit_role: Mapped[bool]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    # One-to-One relationships
    role: Mapped["Role"] = Relationship("Role", back_populates="permissions")

    def __repr__(self):
        return f"""Permission(
            "id": {self.id}
            "create_task": {self.create_task}
            "create_announcement": {self.create_announcement}
            "create_meeting": {self.create_meeting}
            "edit_task": {self.edit_task}
            "edit_announcement": {self.edit_announcement}
            "edit_meeting": {self.edit_meeting}
            "respond_to_task": {self.respond_to_task}
            "set_role": {self.set_role}
            "edit_role": {self.edit_role}
            "role_id": {self.role_id}
        )"""


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    # One-to-One relationships
    permissions: Mapped["Permission"] = Relationship("Permission", back_populates="role")

    def __repr__(self):
        return f"""Role(
            "id": {self.id}
            "name": {self.name}
        )"""


class Division(Base):
    __tablename__ = "divisions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    parent_id: Mapped[int] = mapped_column(ForeignKey("divisions.id"), nullable=True)

    # One-to-Many relationships
    subdivisions: Mapped[List["Division"]] = Relationship("Division", back_populates="parent")
    parent: Mapped["Division"] = Relationship("Division", back_populates="subdivisions", remote_side=[id])
    announcements: Mapped[List["Announcement"]] = Relationship("Announcement", back_populates="division")
    meetings: Mapped[List["Meeting"]] = Relationship("Meeting", back_populates="division")
    assignments: Mapped[List["Assignment"]] = Relationship("Assignment", back_populates="division")

    def __repr__(self):
        return f"""(id: {self.id}, name: {self.name}, parent: {self.parent})"""
