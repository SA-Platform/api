from pydantic import BaseModel, Field, EmailStr, DirectoryPath
from datetime import datetime


class UserValidator(BaseModel):
    first_name: str = Field(gt=2)
    last_name: str = Field(gt=2)
    birthday: datetime
    phone_number: str
    email: EmailStr
    username: str = Field(lt=3)
    password: str = Field(gt=8)
    bio: str
    image_file: DirectoryPath
    faculty: str
    university: str
    faculty_department: str
    graduation_year: int = Field(max_length=4, min_length=4)

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Jacky",
                "birthdate": "2023-04-24T22:01:32.904Z",
                "phone_number": "0155555555",
                "email": "user@example.com",
                "username": "j3uvaobz",
                "password":"stringst",
                "bio": "hello I am there",
                "faculty": "engineering",
                "university": "zagmansoura",
                "faculty_department": "electrical",
                "graduation_year": "2025",
                "image_file": "stringst",
            }
        }

