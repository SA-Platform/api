from pydantic import BaseModel, Field


class FeedbackValidator(BaseModel):
    id: int | None = None
    attachment: str = Field(min_length=2, strip_whitespace=True)
    score: int = Field(gt=0)
    note: str = Field(min_length=2, strip_whitespace=True)

    class Config:
        json_schema_extra = {
            "example": {
                "attachment": "this is an feedback",
                "score": 20,
                "note": "this is really a feedback",
            }
        }
