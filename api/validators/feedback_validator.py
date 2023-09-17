from pydantic import BaseModel, Field


class FeedbackBaseValidator(BaseModel):
    """This model is only used for inheritance"""
    attachment: str = Field(min_length=2, strip_whitespace=True)
    score: int = Field(gt=-1)
    note: str = Field(min_length=2, strip_whitespace=True)


class FeedbackValidator(FeedbackBaseValidator):
    """this model is used for creation as it includes the submission field"""
    submission: int

    class Config:
        json_schema_extra = {
            "example": {
                "submission": 1,
                "attachment": r"C:\Users\amr\Desktop\api",
                "score": 30,
                "note": "create this is really a feedback",
            }
        }


class FeedbackUpdateValidator(FeedbackBaseValidator):
    """this model is used for patch and put requests as it does not include the submission field"""

    class Config:
        json_schema_extra = {
            "example": {
                "attachment": r"C:\Users\amr\Desktop\api",
                "score": 40,
                "note": "Update feedback",
            }
        }
