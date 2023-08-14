from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from enum import Enum


class AnnouncementsCategory(str, Enum):
    INTERNSHIP = "internship"
    EVENT = "event"
    WORKSHOP = "workshop"
    COMPETITION = "competition"
    OTHER = "other"


class UserSignup(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    birthdate: datetime
    phone_number: str
    email: EmailStr
    username: str = Field(min_length=3)
    password: str = Field(min_length=8)
    bio: str
    image_file: str
    faculty: str
    university: str
    faculty_department: str
    graduation_year: int = Field(gt=1900)

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Jacky",
                "birthdate": "2023-04-24T22:01:32.904Z",
                "phone_number": "0155555555",
                "email": "user@example.com",
                "username": "j3uvaobz",
                "password": "stringst",
                "bio": "hello I am there",
                "faculty": "engineering",
                "university": "zagmansoura",
                "faculty_department": "electrical",
                "graduation_year": "2025",
                "image_file": r"C:\Users\omaro\Desktop\api",
            }
        }


class AnnouncementValidator(BaseModel):
    title: str = Field(min_length=2)
    description: str = Field(min_length=2)
    date: datetime
    category: AnnouncementsCategory
    division: str | None = Field(min_length=2)

    @field_validator("date")
    @classmethod
    def validate_date_future(cls, v: datetime) -> datetime:
        if v < datetime.now():
            raise ValueError("date must be in the future")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "this is an announcement",
                "description": "this is really an announcement",
                "date": "2023-04-24T22:01:32.904Z",
                "category": "internship",
                "division": "ras",
            }
        }
