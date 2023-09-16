from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.const import Permissions
from api.crud.sub_feature.excuse import Excuse
from api.db.models import UserModel, AssignmentModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user, CheckPermission
from api.validators import ExcuseValidator, ExcuseBaseValidator

excusesRouter = APIRouter(
    tags=["Excuses"]
)


@excusesRouter.get("/excuses")
async def get_excuses(db: Session = Depends(get_db)):
    return Excuse.get_db_dump(db)


@excusesRouter.post("/excuses")
async def create_excuse(request: ExcuseValidator, db: Session = Depends(get_db),
                        user: UserModel = Depends(CheckPermission(Permissions.CREATE_EXCUSE))):
    return Excuse.create(request, db, user, "assignment", AssignmentModel)


@excusesRouter.put("/excuses/{excuse_id}")
async def update_excuse(excuse_id: int, request: ExcuseBaseValidator, db: Session = Depends(get_db),
                        _: UserModel = Depends(CheckPermission(Permissions.UPDATE_EXCUSE))):
    return Excuse.update(excuse_id, db, **request.model_dump())


@excusesRouter.delete("/excuses/{model_id}")
async def delete_excuse(model_id: int, db: Session = Depends(get_db),
                        _: UserModel = Depends(CheckPermission(Permissions.DELETE_EXCUSE, delete=True,
                                                               model=Excuse.db_model))):
    return Excuse.delete(model_id, db)
