from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, field_validator

from api.validators.username_validator import UsernameValidator


class UserValidator(BaseModel):
    first_name: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True, capitalize=True)
    last_name: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True, capitalize=True)
    birthdate: datetime
    phone_number: str = Field(min_length=7, max_length=15, pattern=r"^(01)[0-9]{9}$", strip_whitespace=True)
    email: EmailStr
    username: str
    password: str = Field(min_length=8)
    bio: str
    faculty: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True, capitalize=True)
    university: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True, capitalize=True)
    faculty_department: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True, capitalize=True)
    graduation_year: int = Field(gt=1900)

    @field_validator("username", mode="before")
    def username_model_validator_call(cls, v):
        UsernameValidator.model_validate({"username": v})
        return v

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
                "graduation_year": "2025"
            }
        }
