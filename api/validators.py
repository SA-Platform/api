from pydantic import BaseModel, Field, EmailStr, DirectoryPath
from datetime import datetime


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
