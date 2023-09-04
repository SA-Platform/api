from pydantic import BaseModel


class HTTPErrorValidator(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }