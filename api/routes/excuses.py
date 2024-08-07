from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.crud.sub_feature.excuse import Excuse
from api.db.models.user_model import UserModel
from api.dependencies import get_db, get_current_user
from api.validators.excuse_validator import ExcuseValidator, ExcuseUpdateValidator

excusesRouter = APIRouter(
    tags=["Excuses"]
)


@excusesRouter.get("/excuses")
async def get_excuses(db: Session = Depends(get_db)):
    return Excuse.get_db_dump(db)


@excusesRouter.post("/excuses")
async def create_excuse(request: ExcuseValidator, db: Session = Depends(get_db),
                        user: UserModel = Depends(get_current_user)):
    return Excuse.create(request, db, user)


@excusesRouter.put("/excuses/{excuse_id}")
async def update_excuse(excuse_id: int, request: ExcuseUpdateValidator, db: Session = Depends(get_db),
                        user: UserModel = Depends(get_current_user)):
    return Excuse.update(excuse_id, db, user, **request.model_dump())


@excusesRouter.delete("/excuses/{model_id}")
async def delete_excuse(model_id: int, db: Session = Depends(get_db),
                        user: UserModel = Depends(get_current_user)):
    return Excuse.delete(model_id, db, user)
