from pydantic import BaseModel, Field


class FeedbackValidator(BaseModel):
    attachment: str = Field(min_length=2, strip_whitespace=True)
    score: int = Field(gt=0)
    note: str = Field(min_length=2, strip_whitespace=True)
    submission: int

    class Config:
        json_schema_extra = {
            "example": {
                "submission": 1,
                "attachment": "this is a feedback",
                "score": 20,
                "note": "this is really a feedback",
            }
        }
