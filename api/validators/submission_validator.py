from pydantic import BaseModel, Field


class SubmissionBaseValidator(BaseModel):
    """ This model is only used for inheritance """

    attachment: str = Field(min_length=2, strip_whitespace=True)
    note: str = Field(min_length=2, strip_whitespace=True)


class SubmissionValidator(SubmissionBaseValidator):
    """this model is used for creation as it includes the assignment field"""
    assignment: int

    class Config:
        json_schema_extra = {
            "example": {
                "assignment": 1,
                "attachment": r"C:\Users\amr\Desktop\api",
                "note": "create this submission",
            }
        }


class SubmissionUpdateValidator(SubmissionBaseValidator):
    """This model is used for patch and put requests as it does not include the assignment field"""

    class Config:
        json_schema_extra = {
            "example": {
                "attachment": r"C:\Users\amr\Desktop\api",
                "note": "update a submission",
            }
        }
