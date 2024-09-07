from pydantic import BaseModel, Field

from api.validators.permission_validator import PermissionValidator


class RoleBaseValidator(BaseModel):
    name: str = Field(min_length=2, strip_whitespace=True)
    permissions: PermissionValidator


class RoleValidator(RoleBaseValidator):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "chairman",
                "permissions": PermissionValidator.Config.json_schema_extra["example"],
            }
        }


class RoleUpdateValidator(RoleBaseValidator):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "member",
                "permissions": PermissionValidator.Config.json_schema_extra["example"],
            }
        }
