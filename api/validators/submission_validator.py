from pydantic import BaseModel, Field


class SubmissionValidator(BaseModel):
    attachment: str = Field(min_length=2, strip_whitespace=True)
    note: str = Field(min_length=2, strip_whitespace=True)
    assignment: int

    class Config:
        json_schema_extra = {
            "example": {
                "assignment": 1,
                "attachment": r"C:\Users\amr\Desktop\api",
                "note": "this is really an submission",
            }
        }
