from pydantic import BaseModel, Field


class DivisionValidator(BaseModel):
    name: str = Field(min_length=2, strip_whitespace=True, strict=True)
    parent: str | None = Field(default=None, min_length=2, strip_whitespace=True, strict=True)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "CS",
                "parent": "IEEE"
            }
        }
