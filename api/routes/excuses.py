from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.const import FeaturePermissions
from api.crud.sub_feature.excuse import Excuse
from api.db.models import UserModel, AssignmentModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user, CheckPermission
from api.validators import ExcuseValidator, ExcuseUpdateValidator

excusesRouter = APIRouter(
    tags=["Excuses"]
)


@excusesRouter.get("/excuses")
async def get_excuses(db: Session = Depends(get_db)):
    return Excuse.get_db_dump(db)


@excusesRouter.post("/excuses")
async def create_excuse(request: ExcuseValidator, division_id: int, db: Session = Depends(get_db),
                        user: UserModel = Depends(CheckPermission(FeaturePermissions.CREATE_EXCUSE))):
    return Excuse.create(request, db, user, "assignment", AssignmentModel)


@excusesRouter.put("/excuses/{excuse_id}/{division_id}")
async def update_excuse(excuse_id: int, division_id: int, request: ExcuseUpdateValidator, db: Session = Depends(get_db),
                        user: UserModel = Depends(get_current_user)):
    return Excuse.update(excuse_id, request, db, division_id, user)


@excusesRouter.delete("/excuses/{model_id}/{division_id}")
async def delete_excuse(model_id: int, division_id: int, db: Session = Depends(get_db),
                        user: UserModel = Depends(get_current_user)):
    return Excuse.delete(model_id, db, user)
