from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.db.models import UserModel
from api.dependencies import get_db, get_current_user
from api.routes.features_base import Role
from api.validators import RoleValidator

rolesRouter: APIRouter = APIRouter(
    tags=["Roles"]
)


@rolesRouter.get(path="/roles", dependencies=[Depends(get_current_user)])
async def get_roles(db: Session = Depends(get_db)):
    return Role.get_db_dump(db)


@rolesRouter.post(path="/roles", dependencies=[Depends(get_current_user)])
async def create_role(request: RoleValidator, db: Session = Depends(get_db)):
    return Role.create(request, db)


@rolesRouter.put(path="/roles/{role_id}", dependencies=[Depends(get_current_user)])
async def update_role(role_id: int, request: RoleValidator, db: Session = Depends(get_db)):
    return Role.update(role_id, request, db)


@rolesRouter.delete(path="/roles/{role_id}", dependencies=[Depends(get_current_user)])
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    return Role.delete(role_id, db)
