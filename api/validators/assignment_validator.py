from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


class AssignmentValidator(BaseModel):
    title: str = Field(min_length=2, strip_whitespace=True)
    description: str = Field(min_length=2, strip_whitespace=True)
    deadline: datetime
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
                "weight": "20",
                "division": "CS",
            }
        }
