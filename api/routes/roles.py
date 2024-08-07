from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.const import CorePermissions
from api.crud.core.role import Role
from api.db.models.user_model import UserModel
from api.dependencies import get_db, get_current_user, CheckPermission
from api.validators.role_validator import RoleValidator, RoleUpdateValidator

rolesRouter: APIRouter = APIRouter(
    tags=["Roles"]
)


@rolesRouter.get(path="/roles", dependencies=[Depends(get_current_user)])
async def get_roles(db: Session = Depends(get_db)):
    return Role.get_db_dump(db)


@rolesRouter.post(path="/roles")
async def create_role(request: RoleValidator,
                      db: Session = Depends(get_db),
                      _: UserModel = Depends(CheckPermission(CorePermissions.CREATE_ROLE, core=True))):
    return Role.create(db, **request.model_dump())


@rolesRouter.put(path="/roles/{role_id}")
async def update_role(role_id: int, request: RoleUpdateValidator, db: Session = Depends(get_db),
                      _: UserModel = Depends(CheckPermission(CorePermissions.UPDATE_ROLE, core=True))):
    return Role.update(role_id, db, **request.model_dump())


@rolesRouter.delete(path="/roles/{role_id}", dependencies=[Depends(get_current_user)])
async def delete_role(role_id: int, db: Session = Depends(get_db),
                      _: UserModel = Depends(CheckPermission(CorePermissions.DELETE_ROLE, core=True))):
    return Role.delete(role_id, db)
