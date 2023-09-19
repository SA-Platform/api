from pydantic import BaseModel


class PermissionValidator(BaseModel):
    pass


class CorePermissionValidator(PermissionValidator):
    UPDATE_USER: bool
    DELETE_USER: bool
    CREATE_DIVISION: bool
    UPDATE_DIVISION: bool
    DELETE_DIVISION: bool
    CREATE_ROLE: bool
    UPDATE_ROLE: bool
    DELETE_ROLE: bool

    class Config:
        json_schema_extra = {
            "example": {
                        "UPDATE_USER": True,
                        "DELETE_USER": True,
                        "CREATE_DIVISION": True,
                        "UPDATE_DIVISION": True,
                        "DELETE_DIVISION": True,
                        "CREATE_ROLE": True,
                        "UPDATE_ROLE": True,
                        "DELETE_ROLE": True
                    }
            }


class FeaturePermissionValidator(PermissionValidator):
    CREATE_ASSIGNMENT: bool
    UPDATE_ASSIGNMENT: bool
    DELETE_ASSIGNMENT: bool
    CREATE_ANNOUNCEMENT: bool
    UPDATE_ANNOUNCEMENT: bool
    DELETE_ANNOUNCEMENT: bool
    CREATE_MEETING: bool
    UPDATE_MEETING: bool
    DELETE_MEETING: bool
    CREATE_SUBMISSION: bool
    UPDATE_SUBMISSION: bool
    DELETE_SUBMISSION: bool
    CREATE_EXCUSE: bool
    UPDATE_EXCUSE: bool
    DELETE_EXCUSE: bool
    CREATE_FEEDBACK: bool
    UPDATE_FEEDBACK: bool
    DELETE_FEEDBACK: bool

    class Config:
        json_schema_extra = {
            "example": {
                    "CREATE_ASSIGNMENT": True,
                    "UPDATE_ASSIGNMENT": True,
                    "DELETE_ASSIGNMENT": True,
                    "CREATE_ANNOUNCEMENT": True,
                    "UPDATE_ANNOUNCEMENT": True,
                    "DELETE_ANNOUNCEMENT": True,
                    "CREATE_MEETING": True,
                    "UPDATE_MEETING": True,
                    "DELETE_MEETING": True,
                    "CREATE_SUBMISSION": True,
                    "UPDATE_SUBMISSION": True,
                    "DELETE_SUBMISSION": True,
                    "CREATE_EXCUSE": True,
                    "UPDATE_EXCUSE": True,
                    "DELETE_EXCUSE": True,
                    "CREATE_FEEDBACK": True,
                    "UPDATE_FEEDBACK": True,
                    "DELETE_FEEDBACK": True
                }
            }
