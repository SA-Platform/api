from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from api.const import FeaturePermissions
from api.crud.feature.assignment import Assignment
from api.db.models import UserModel  # unresolved reference ignored
from api.dependencies import get_current_user, get_db, CheckPermission
from api.validators import AssignmentValidator, AssignmentUpdateValidator

assignmentsRouter = APIRouter(
    tags=["Assignments"]
)


@assignmentsRouter.get("/assignments")
async def get_assignments(db: Session = Depends(get_db),
                          _: UserModel = Depends(get_current_user)):
    return Assignment.get_db_dump(db)


@assignmentsRouter.post("/assignments/{division_id}", status_code=status.HTTP_201_CREATED)
async def create_assignment(division_id: int, request: AssignmentValidator, db: Session = Depends(get_db),
                            user: UserModel = Depends(CheckPermission(FeaturePermissions.CREATE_ASSIGNMENT))):
    return Assignment.create(request, db, user, division_id)


@assignmentsRouter.put("/assignments/{assignment_id}/{division_id}")
async def update_assignment(assignment_id: int, request: AssignmentUpdateValidator, division_id: int,
                            db: Session = Depends(get_db),
                            user: UserModel = Depends(CheckPermission(FeaturePermissions.UPDATE_ASSIGNMENT))):
    return Assignment.update(assignment_id, request, db, division_id, user)


@assignmentsRouter.delete("/assignments/{assignment_id}/{division_id}")
async def delete_assignment(assignment_id: int, division_id: int, db: Session = Depends(get_db),
                            user: UserModel = Depends(CheckPermission(FeaturePermissions.DELETE_ASSIGNMENT))):
    return Assignment.delete(assignment_id, db, user)
