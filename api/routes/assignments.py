from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from api.crud.feature.assignment import Assignment
from api.db.models.user_model import UserModel
from api.dependencies import get_current_user, get_db
from api.validators.assignment_validator import AssignmentValidator, AssignmentUpdateValidator

assignmentsRouter = APIRouter(
    tags=["Assignments"]
)


@assignmentsRouter.get("/assignments")
async def get_assignments(db: Session = Depends(get_db),
                          _: UserModel = Depends(get_current_user)):
    return Assignment.get_db_dump(db)


@assignmentsRouter.post("/assignments", status_code=status.HTTP_201_CREATED)
async def create_assignment(request: AssignmentValidator, db: Session = Depends(get_db),
                            user: UserModel = Depends(get_current_user)):
    return Assignment.create(request, db, user)


@assignmentsRouter.put("/assignments/{assignment_id}")
async def update_assignment(assignment_id: int, request: AssignmentUpdateValidator, db: Session = Depends(get_db),
                            user: UserModel = Depends(get_current_user)):
    return Assignment.update(assignment_id, request, db, user)


@assignmentsRouter.delete("/assignments/{model_id}")
async def delete_assignment(model_id: int, db: Session = Depends(get_db),
                            user: UserModel = Depends(get_current_user)):
    return Assignment.delete(model_id, db, user)
