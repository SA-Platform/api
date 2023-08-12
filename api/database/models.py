from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, BigInteger, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(DateTime(timezone=True))
    phone_number = Column(String, nullable=True)
    email = Column(String)
    faculty = Column(String)
    university = Column(String)
    faculty_department = Column(String)
    graduation_year = Column(Integer)
    image_file = Column(String)
    bio = Column(String, nullable=True)
    confirmed = Column(Boolean, default=False)
    username = Column(String)
    date_created = Column(DateTime(timezone=True))
    password = Column(String)

    # One-to-One relationship
    user_role_division = relationship("UserRoleDivision", back_populates="user")

    # One-to-Many relationships
    announcements = relationship("Announcement", back_populates="user", lazy='dynamic')
    feedbacks = relationship("Feedback", back_populates="user", lazy='dynamic')
    submissions = relationship("Submission", back_populates="user", lazy='dynamic')
    meeting = relationship("Meeting", back_populates="user", lazy='dynamic')
    excuses = relationship("Excuse", back_populates="user", lazy='dynamic')
    assignments = relationship("Assignment", back_populates="user", lazy='dynamic')

    def __str__(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "birthday": self.birthday,
            "phone_number": self.phone_number,
            "email": self.email,
            "faculty": self.faculty,
            "university": self.university,
            "faculty_department": self.faculty_department,
            "graduation_year": self.graduation_year,
            "image_file": self.image_file,
            "bio": self.bio,
            "confirmed": self.confirmed,
            "username": self.username,
            "date_created": self.date_created,
            "password": self.password,
        }


class Announcement(Base):
    __tablename__ = "announcement"

    id = Column(BigInteger, primary_key=True)
    date_created = Column(DateTime(timezone=True))
    date = Column(DateTime(timezone=True), nullable=True)
    category = Column(String)
    title = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    division_id = Column(BigInteger, ForeignKey("division.id", ondelete="CASCADE", onupdate="CASCADE"))

    # One-to-Many relationships
    user = relationship("User", back_populates="announcements", lazy='dynamic')
    division = relationship("Division", back_populates="announcements", lazy='dynamic')

    def __str__(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "division_id": self.division_id,
            "date_created": self.date_created,
            "date": self.date,
            "category": self.category,
            "title": self.title,
            "description": self.description,
        }


class Meeting(Base):
    __tablename__ = "meeting"

    id = Column(BigInteger, primary_key=True)
    title = Column(String)
    description = Column(String)
    date_created = Column(DateTime(timezone=True))
    latitude = Column(Float(precision=6), nullable=True)
    longitude = Column(Float(precision=6), nullable=True)
    location_text = Column(String, nullable=True)
    type = Column(String)
    division_id = Column(BigInteger, ForeignKey("division.id", ondelete="CASCADE", onupdate="CASCADE"))
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))

    # One-to-Many relationships
    user = relationship("User", back_populates="meeting", lazy='dynamic')
    division = relationship("Division", back_populates="meeting", lazy='dynamic')

    def __str__(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date_created": self.date_created,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "location_text": self.location_text,
            "division_id": self.division_id,
            "user_id": self.user_id,
            "type": self.type,

        }


class Division(Base):
    __tablename__ = "division"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    parent = Column(String, nullable=True)

    # One-to-One relationship
    userRoleDivision = relationship("UserRoleDivision", back_populates="division")

    # One-to-Many relationships
    announcements = relationship("Announcement", back_populates="division", lazy='dynamic')
    meetings = relationship("Meeting", back_populates="division", lazy='dynamic')
    assignments = relationship("Assignment", back_populates="division", lazy='dynamic')

    def __str__(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent": self.parent,

        }


class Role(Base):
    __tablename__ = "role"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)

    # One-to-One relationship
    userRoleDivision = relationship("UserRoleDivision", back_populates="role")

    def __str__(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class UserRoleDivision(Base):
    __tablename__ = "user_role_division"

    id = Column(BigInteger, primary_key=True)
    role_id = Column(BigInteger, ForeignKey("role.id", ondelete="CASCADE", onupdate="CASCADE"))
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    division_id = Column(BigInteger, ForeignKey("division.id", ondelete="CASCADE", onupdate="CASCADE"))

    # One-to-One relationships
    user = relationship("User", back_populates="user_role_division")
    role = relationship("Role", back_populates="user_role_division")
    division = relationship("Division", back_populates="user_role_division")

    def __str__(self):
        return {
            "id": self.id,
            "role_id": self.role_id,
            "user_id": self.user_id,
            "division_id": self.division_id,
        }


class Assignment(Base):
    __tablename__ = "assignment"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    division_id = Column(BigInteger, ForeignKey("division.id", ondelete="CASCADE", onupdate="CASCADE"))
    title = Column(String)
    description = Column(String)
    date_created = Column(DateTime(timezone=True))
    deadline = Column(DateTime(timezone=True))
    attachment = Column(String, nullable=True)
    weight = Column(Integer)

    # One-to-Many relationships
    user = relationship("User", back_populates="assignment", lazy='dynamic')
    division = relationship("Division", back_populates="assignment", lazy='dynamic')
    submission = relationship("Submission", back_populates="assignment", lazy='dynamic')
    excuse = relationship("Excuse", back_populates="assignment", lazy='dynamic')

    def __str__(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "division_id": self.division_id,
            "title": self.title,
            "description": self.description,
            "date_created": self.date_created,
            "deadline": self.deadline,
            "attachment": self.attachment,
            "weight": self.weight,

        }


class Excuse(Base):
    __tablename__ = "excuse"
    id = Column(BigInteger, primary_key=True)
    description = Column(String)
    date_created = Column(DateTime(timezone=True))
    validity = Column(DateTime(timezone=True))
    accepted = Column(Boolean, nullable=True, default=False)
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    assignment_id = Column(BigInteger, ForeignKey("assignment.id", ondelete="CASCADE", onupdate="CASCADE"))

    # One-to-Many relationships
    user = relationship("User", back_populates="excuse", lazy='dynamic')
    assignment = relationship("Assignment", back_populates="excuse", lazy='dynamic')

    def __str__(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "assignment_id": self.assignment_id,
            "description": self.description,
            "date_created": self.date_created,
            "validity": self.validity,
            "accepted": self.accepted,

        }


class Submission(Base):
    __tablename__ = "submission"

    id = Column(BigInteger, primary_key=True)
    attachment = Column(String)
    note = Column(String)
    date_created = Column(DateTime(timezone=True))
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    assignment_id = Column(BigInteger, ForeignKey("assignment.id", ondelete="CASCADE", onupdate="CASCADE"))

    # One-to-Many relationships
    user = relationship("User", back_populates="submission", lazy='dynamic')
    assignment = relationship("Assignment", back_populates="submission", lazy='dynamic')
    feedback = relationship("Feedback", back_populates="submission", lazy='dynamic')

    def __str__(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "assignment_id": self.assignment_id,
            "attachment": self.attachment,
            "date_created": self.date_created,
            "note": self.note,

        }


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(BigInteger, primary_key=True)
    attachment = Column(String)
    score = Column(BigInteger)
    note = Column(String)
    date_created = Column(DateTime(timezone=True))
    user_id = Column(BigInteger, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"))
    submission_id = Column(BigInteger, ForeignKey("submission.id", ondelete="CASCADE", onupdate="CASCADE"))

    # One-to-Many relationships
    user = relationship("User", back_populates="feedback", lazy='dynamic')
    submission = relationship("Submission", back_populates="feedback", lazy='dynamic')

    def __str__(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "submission_id": self.submission_id,
            "attachment": self.attachment,
            "score": self.score,
            "note": self.note,
            "date_created": self.date_created,

        }
