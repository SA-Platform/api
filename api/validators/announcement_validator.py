from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator

from api.const import AnnouncementsCategory


class AnnouncementBaseValidator(BaseModel):
    title: str = Field(min_length=2, strip_whitespace=True)
    description: str = Field(min_length=2, strip_whitespace=True)
    date: datetime | None
    category: AnnouncementsCategory

    @field_validator("date")
    def validate_date_future(cls, v: datetime) -> datetime:
        if v < datetime.now(timezone.utc):
            raise ValueError("date must be in the future")
        return v


class AnnouncementValidator(AnnouncementBaseValidator):
    class Config:
        json_schema_extra = {
            "example": {
                "title": "this is an announcement",
                "description": "this is really an announcement",
                "date": "2025-04-24T22:01:32.904Z",
                "category": "internship",
            }
        }


class AnnouncementUpdateValidator(AnnouncementBaseValidator):
    class Config:
        json_schema_extra = {
            "example": {
                "title": "update the  announcement",
                "description": "update the announcement",
                "date": "2025-04-24T22:01:32.904Z",
                "category": "event",
            }
        }
