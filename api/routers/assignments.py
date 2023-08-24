from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.db.models import User, Assignment
from api.validators import AssignmentValidator

from api.routers.features_base import Base

assignmentsHandler = Base("assignment", "Assignments", AssignmentValidator, Assignment)
assignmentsRouter: APIRouter = assignmentsHandler.router


@assignmentsRouter.get(assignmentsHandler.path)
async def get_assignments(db: Session = Depends(get_db),
                          _: User = Depends(get_current_user)):
    return assignmentsHandler.get_all(db)


@assignmentsRouter.post(assignmentsHandler.path, status_code=status.HTTP_201_CREATED)
async def create_assignment(request: AssignmentValidator, db: Session = Depends(get_db),
                            user: User = Depends(get_current_user)):
    return assignmentsHandler.create(request, db, user)


@assignmentsRouter.put(assignmentsHandler.path)
async def update_assignment(request: AssignmentValidator, db: Session = Depends(get_db),
                            _: User = Depends(get_current_user)):
    return assignmentsHandler.update(request, db)


@assignmentsRouter.delete(assignmentsHandler.path)
async def delete_assignment(assignment_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return assignmentsHandler.delete(assignment_id, db)
