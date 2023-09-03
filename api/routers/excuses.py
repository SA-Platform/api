from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.models.core_models import UserModel
from api.dependencies import get_db, get_current_user
from api.routers.features_base import Excuse
from api.validators import ExcuseValidator

excusesRouter = Excuse.router


@excusesRouter.get(Excuse.path)
async def get_excuses(db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Excuse.get_db_dump(db)


@excusesRouter.post(Excuse.path)
async def post_excuse(request: ExcuseValidator, db: Session = Depends(get_db),
                      user: UserModel = Depends(get_current_user)):
    return Excuse.create(request, db, user)


@excusesRouter.put(Excuse.path)
async def update_excuse(request: ExcuseValidator, db: Session = Depends(get_db),
                        _: UserModel = Depends(get_current_user)):
    return Excuse.update(request, db)


@excusesRouter.delete(Excuse.path)
async def delete_excuse(excuse_id: int, db: Session = Depends(get_db),
                        _: UserModel = Depends(get_current_user)):
    return Excuse.delete(excuse_id, db)
