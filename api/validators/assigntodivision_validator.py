from typing import Optional

from pydantic import BaseModel, Field


class AssignToDivisionValidator(BaseModel):
    role_id: Optional[int] = Field(ge=0, nullable=True)

    class Config:
        json_schema_extra = {
            "example": {
                "role_id": 0
            }
        }
