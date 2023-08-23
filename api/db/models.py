import datetime
from typing import List

import bcrypt
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, Float
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Relationship
from api.const import AnnouncementsCategory


class Base(DeclarativeBase):
    pass


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
    image_file: Mapped[str] = mapped_column(String)
    bio: Mapped[str] = mapped_column(String, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())

    # One-to-Many relationships
    announcements: Mapped[List["Announcement"]] = Relationship("Announcement", back_populates="creator")
    meetings: Mapped[List["Meeting"]] = Relationship("Meeting", back_populates="creator")
    assignments: Mapped[List["Assignment"]] = Relationship("Assignment", back_populates="creator")
    excuse: Mapped[List["Excuse"]] = Relationship("Excuse", back_populates="creator")
    submission: Mapped[List["Submission"]] = Relationship("Submission", back_populates="creator")
    feedback: Mapped[List["Feedback"]] = Relationship("Feedback", back_populates="creator")

    def set_password(self, password) -> str:
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        return self.password

    def check_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def __init__(self, first_name: str, last_name: str, birthdate: datetime.datetime,
                 phone_number: str, email: str, username: str, password: str,
                 faculty: str, university: str, faculty_department: str,
                 graduation_year: int, image_file: str, bio: str = None) -> None:
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
               location_lat: float | None, location_long: float | None, division: Division) -> None:
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
               division: Division) -> None:
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
    submission: Mapped["Submission"] = Relationship("Submission", back_populates="assignments")
    excuse: Mapped["Excuse"] = Relationship("Excuse", back_populates="assignments")

    def update(self, title: str, description: str, deadline: datetime, attachment: str,
               weight: int, division: Division) -> None:
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
    creator: Mapped["User"] = Relationship("User", back_populates="excuse")
    assignments: Mapped["Assignment"] = Relationship("Assignment", back_populates="excuse")

    def __repr__(self):
        return f"""Permission(
                "id": {self.id},
                "creator_id": {self.creator_id},
                "assignment_id": {self.assignment_id},
                "description": {self.description},
                "validity": {self.validity},
                "accepted": {self.accepted},
            )"""


class Submission(Base):
    __tablename__ = "submission"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assignment_id: Mapped[int] = mapped_column(ForeignKey("assignments.id"))
    attachment: Mapped[str] = mapped_column(String, nullable=True)
    note: Mapped[str] = mapped_column(String)
    date_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now())

    # Many-to-One relationships
    creator: Mapped["User"] = Relationship("User", back_populates="submission")
    assignments: Mapped["Assignment"] = Relationship("Assignment", back_populates="submission")
    feedback: Mapped["Feedback"] = Relationship("Feedback", back_populates="submission")

    def __repr__(self):
        return f"""Permission(
                "id": {self.id},
                "creator_id": {self.creator_id},
                "assignment_id": {self.assignment_id},
                "note": {self.note},
                "attachment": {self.attachment},
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
