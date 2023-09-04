from pydantic import BaseModel, Field


class SubmissionValidator(BaseModel):
    id: int | None = None
    attachment: str = Field(min_length=2, strip_whitespace=True)
    note: str = Field(min_length=2, strip_whitespace=True)

    class Config:
        json_schema_extra = {
            "example": {
                "attachment": r"C:\Users\amr\Desktop\api",
                "note": "this is really an submission",
            }
        }
