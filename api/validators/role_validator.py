from pydantic import BaseModel, Field, field_validator


class RoleValidator(BaseModel):
    id: int | None = None
    name: str = Field(min_length=2, strip_whitespace=True)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "chairman",
            }
        }
