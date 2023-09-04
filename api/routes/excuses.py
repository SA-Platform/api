from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.db.models import UserModel   # unresolved reference ignored
from api.dependencies import get_db, get_current_user
from api.routes.features_base import Excuse

excusesRouter = APIRouter(
    tags=["Excuses"]
)


@excusesRouter.get("/excuses")
async def get_excuses(db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Excuse.get_db_dump(db)


@excusesRouter.post("/excuses")
async def post_excuse(request: Excuse.validator, db: Session = Depends(get_db),
                      user: UserModel = Depends(get_current_user)):
    return Excuse.create(request, db, user)


@excusesRouter.put("/excuses")
async def update_excuse(request: Excuse.validator, db: Session = Depends(get_db),
                        _: UserModel = Depends(get_current_user)):
    return Excuse.update(request, db)


@excusesRouter.delete("/excuses")
async def delete_excuse(excuse_id: int, db: Session = Depends(get_db),
                        _: UserModel = Depends(get_current_user)):
    return Excuse.delete(excuse_id, db)
