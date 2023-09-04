from pydantic import BaseModel, Field


class UsernameValidator(BaseModel):
    username: str = Field(...,
                          min_length=2,
                          strip_whitespace=True,
                          pattern=r"^[a-zA-Z0-9_]*$",
                          to_lower=True,
                          strict=True)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "twibster0x_11"
            }
        }


