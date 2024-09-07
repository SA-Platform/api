from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


class ExcuseBaseValidator(BaseModel):
    """This model is only used for inheritance"""

    description: str = Field(min_length=2, strip_whitespace=True)
    validity: datetime

    @field_validator("validity")
    def validate_date_future(cls, v: datetime) -> datetime:
        if v < datetime.now(timezone.utc):
            raise ValueError("date must be in the future")
        return v


class ExcuseValidator(ExcuseBaseValidator):
    """this model is used for creation as it includes the assignment field"""

    assignment: int

    class Config:
        json_schema_extra = {
            "example": {
                "assignment": 1,
                "description": "this is really an assignment",
                "validity": "2025-04-24T22:01:32.904Z",
            }
        }


class ExcuseUpdateValidator(ExcuseBaseValidator):
    """This model is used for patch and put requests as it does not include the assignment field"""

    class Config:
        json_schema_extra = {
            "example": {
                "description": "this is and edit, dude",
                "validity": "2027-04-24T22:01:32.904Z",
            }
        }
