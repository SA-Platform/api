from pydantic import BaseModel, Field


class DivisionBaseValidator(BaseModel):
    name: str = Field(min_length=2, strip_whitespace=True, strict=True)
    parent: str | None = Field(default=None, min_length=2, strip_whitespace=True, strict=True)


class DivisionValidator(DivisionBaseValidator):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "CS",
                "parent": "IEEE"
            }
        }


class DivisionUpdateValidator(DivisionBaseValidator):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "CS",
                "parent": "RAS"
            }
        }
