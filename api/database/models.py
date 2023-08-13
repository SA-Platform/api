import datetime

from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


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

    def __repr__(self):
        return f"""User(
            "id": {self.id}
            "first_name": {self.first_name}
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
