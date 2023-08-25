from pydantic import (BaseModel,
                      Field,
                      EmailStr,
                      field_validator,
                      model_validator)
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from api.const import AnnouncementsCategory

from api.db.models import Division
from api.dependencies import get_db


class Message(BaseModel):
    message: str


class HTTPError(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }


class UserValidator(BaseModel):
    first_name: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True, capitalize=True)
    last_name: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True, capitalize=True)
    birthdate: datetime
    phone_number: str = Field(min_length=11, max_length=11, pattern=r"^(01)[0-9]{9}$", strip_whitespace=True)
    email: EmailStr
    username: str = Field(min_length=3, strip_whitespace=True, pattern=r"^[a-zA-Z0-9_]*$", to_lower=True, strict=True)
    password: str = Field(min_length=8)
    bio: str
    # image_file: str
    faculty: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True, capitalize=True)
    university: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True, capitalize=True)
    faculty_department: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True, capitalize=True)
    graduation_year: int = Field(gt=1900)

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Jacky",
                "birthdate": "2023-04-24T22:01:32.904Z",
                "phone_number": "01234567891",
                "email": "user@example.com",
                "username": "j3uvaobz",
                "password": "stringst",
                "bio": "hello I am there",
                "faculty": "engineering",
                "university": "zagmansoura",
                "faculty_department": "electrical",
                "graduation_year": "2025",
                # "image_file": r"C:\Users\omaro\Desktop\api",
            }
        }


class AnnouncementValidator(BaseModel):
    id: int | None = None
    title: str = Field(min_length=2, strip_whitespace=True)
    description: str = Field(min_length=2, strip_whitespace=True)
    date: datetime | None
    category: AnnouncementsCategory
    division: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True)

    @field_validator("date")
    def validate_date_future(cls, v: datetime) -> datetime:
        if v < datetime.now(timezone.utc):
            raise ValueError("date must be in the future")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "this is an announcement",
                "description": "this is really an announcement",
                "date": "2025-04-24T22:01:32.904Z",
                "category": "internship",
                "division": "ras",
            }
        }


class MeetingValidator(BaseModel):
    id: int | None = None
    title: str = Field(min_length=2, strip_whitespace=True)
    description: str = Field(min_length=2)
    date: datetime
    location_text: str | None = None
    location_lat: float | None = None
    location_long: float | None = None
    division: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True)

    @field_validator("date")
    def validate_date_future(cls, v: datetime) -> datetime:
        if v < datetime.now(timezone.utc):
            raise ValueError("date must be in the future")
        return v

    @field_validator("location_lat", "location_long")
    def check_precision(cls, value: float) -> float:
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
                "date": "2025-04-24T22:01:32.904Z",
                "location_text": "our lovely college",
                "location_long": "30.586388",
                "location_lat": "31.482434",
                "division": "CS",
            }
        }


class DivisionValidator(BaseModel):
    id: int | None = None
    name: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True)
    parent: str | None = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True)

    @model_validator(mode="after")
    def division_exists(self) -> "DivisionValidator":
        db: Session = next(get_db())
        division = db.query(Division).filter_by(name=self.name).first()
        parent = db.query(Division).filter_by(name=self.parent).first()
        if self.name == self.parent:
            raise ValueError("division can't be its own parent")
        elif self.parent:
            if not parent:
                raise ValueError("parent division doesn't exist")
            elif division:
                if division.parent == parent:
                    raise ValueError(f"division {division.name} with the same parent ({parent.name}) already exists")
                elif not division.parent:
                    raise ValueError(f"division {division.name} is a root division and can't have a parent")
            return self
        else:
            if division:
                raise ValueError(f"division {division.name} already exists")
            elif not self.id:
                root = db.query(Division).filter_by(parent=None).first()
                if root:
                    raise ValueError(f"only one root division is allowed, which is {root.name}")
            return self

    class Config:
        json_schema_extra = {
            "example": {
                "name": "CS",
                "parent": "IEEE",
            }
        }


class UsernameValidator(BaseModel):
    username: str = Field(...,
                          min_length=2,
                          strip_whitespace=True,
                          pattern=r"^[a-zA-Z0-9_]*$",
                          to_lower=True,
                          strict=True)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "twibster0x_11"
            }
        }


class AssignmentValidator(BaseModel):
    id: int | None = None
    title: str = Field(min_length=2, strip_whitespace=True)
    description: str = Field(min_length=2, strip_whitespace=True)
    deadline: datetime
    # attachment: str | None = None
    weight: int = Field(gt=0)
    division: str = Field(min_length=2)

    @field_validator("deadline")
    def validate_date_future(cls, v: datetime) -> datetime:
        if v < datetime.now(timezone.utc):
            raise ValueError("date must be in the future")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "this is an assignment",
                "description": "this is really an assignment",
                "deadline": "2025-04-24T22:01:32.904Z",
                # "attachment": "assignment.pdf",
                "weight": "20",
                "division": "CS",
            }
        }
