from pydantic import BaseModel, Field


class DivisionValidator(BaseModel):
    name: str = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True)
    parent: str | None = Field(min_length=2, strip_whitespace=True, to_lower=True, strict=True)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "CS",
                "parent": "IEEE",
            }
        }
