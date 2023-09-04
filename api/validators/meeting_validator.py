from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


class MeetingValidator(BaseModel):
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