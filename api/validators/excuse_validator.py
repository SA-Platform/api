from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


class ExcuseValidator(BaseModel):
    id: int | None = None
    title: str = Field(min_length=2, strip_whitespace=True)
    description: str = Field(min_length=2, strip_whitespace=True)
    validity: datetime
    accepted: bool

    @field_validator("validity")
    def validate_date_future(cls, v: datetime) -> datetime:
        if v < datetime.now(timezone.utc):
            raise ValueError("date must be in the future")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "this is an assignment",
                "description": "this is really an assignment",
                "validity": "2025-04-24T22:01:32.904Z",
                "accepted": "True",
            }
        }
