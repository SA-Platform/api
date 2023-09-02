from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.db.models.core_models import UserModel
from api.validators import AssignmentValidator
from api.routers.features_base import Assignment

assignmentsRouter: APIRouter = Assignment.router


@assignmentsRouter.get(Assignment.path)
async def get_assignments(db: Session = Depends(get_db),
                          _: UserModel = Depends(get_current_user)):
    return Assignment.get_db_dump(db)


@assignmentsRouter.post(Assignment.path, status_code=status.HTTP_201_CREATED)
async def create_assignment(request: AssignmentValidator, db: Session = Depends(get_db),
                            user: UserModel = Depends(get_current_user)):
    return Assignment.create(request, db, user)


@assignmentsRouter.put(Assignment.path)
async def update_assignment(request: AssignmentValidator, db: Session = Depends(get_db),
                            _: UserModel = Depends(get_current_user)):
    return Assignment.update(request, db)


@assignmentsRouter.delete(Assignment.path)
async def delete_assignment(assignment_id: int, db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Assignment.delete(assignment_id, db)
