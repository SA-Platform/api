from pydantic import BaseModel, Field


class RoleValidator(BaseModel):
    name: str = Field(min_length=2, strip_whitespace=True)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "chairman",
            }
        }
