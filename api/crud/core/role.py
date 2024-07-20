from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .core_base import CoreBase
from ...db.models.role_model import RoleModel


class Role(CoreBase):
    db_model = RoleModel

    @classmethod
    def create(cls, db: Session, **kwargs) -> RoleModel:
        cls.check_role_exists(db, kwargs.get("name"))
        return super().create(db, name=kwargs["name"])
        # permissions=cls._calculate_total_permission(kwargs["permissions"]))

    @classmethod
    def update(cls, model_id: int, db: Session, **kwargs) -> RoleModel:
        model = cls.get_db_first(db, "id", model_id)
        if model:
            role_found = cls.get_db_first(db, "name", kwargs["name"])
            if role_found and role_found.id != model_id:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="role already exists")
            model.name = kwargs["name"]
            # model.permissions = cls._calculate_total_permission(kwargs["permissions"])
            db.commit()
            db.refresh(model)
            return model
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__.lower()} not found")

    @classmethod
    def check_role_exists(cls, db: Session, name: str) -> None:
        role = cls.get_db_first(db, "name", name)
        if role:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="role already exists")

    # @classmethod
    # def _calculate_total_permission(cls, request_permissions: dict) -> int:
    #     total_request: int = 0
    #     for permission in CorePermission:
    #         if request_permissions[permission.name]:
    #             total_request = total_request | permission.value
    #     return total_request
