from _pydecimal import Decimal

from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from enum import Enum

from pydantic.v1 import confloat, validator


class AnnouncementsCategory(str, Enum):
    INTERNSHIP = "internship"
    EVENT = "event"
    WORKSHOP = "workshop"
    COMPETITION = "competition"
    OTHER = "other"


class UserValidator(BaseModel):
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


class MeetingValidator(BaseModel):
    title: str = Field(min_length=2)
    description: str = Field(min_length=2)
    location_text: str | None = Field(min_length=2)
    location_lat: float = Field(ge=-90.0, le=90.0)
    location_long: float = Field(ge=-180.0, le=180.0)
    creator: str = Field(min_length=2)
    division: str = Field(min_length=2)

    @validator("location_lat", "location_long", pre=True, always=True)
    def check_precision(self, value: float) -> float:
        if isinstance(value, float):
            precision = len(str(value).split('.')[-1])
            if precision < 6:
                raise ValueError("Float value must have at least 6 decimal places.")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "title": "this is an meeting",
                "description": "this is really an meeting",
                "location_text": "our lovely college",
                "location_long": "30.586388",
                "location_lat": "31.482434",
                "creator": "J3uvaobz",
                "division": "CS",
            }
        }
