from pydantic import BaseModel, Field

from api.validators.permission_validator import FeaturePermissionValidator


class RoleBaseValidator(BaseModel):
    name: str = Field(min_length=2, strip_whitespace=True)
    division_id: int = Field(ge=0)
    permissions: FeaturePermissionValidator


class RoleValidator(RoleBaseValidator):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "chairman",
                "division_id": 1,
                "permissions":
                    FeaturePermissionValidator.Config.json_schema_extra["example"]
            }
        }


class RoleUpdateValidator(RoleBaseValidator):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "member",
                "division_id": 1,
                "permissions":
                    FeaturePermissionValidator.Config.json_schema_extra["example"]
            }
        }
