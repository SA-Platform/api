from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.db.models import User, Assignment, Division
from api.validators import AssignmentValidator

assignmentsRouter: APIRouter = APIRouter(
    tags=["Assignments"]
)


@assignmentsRouter.get("/assignments", )
async def get_assignments(db: Session = Depends(get_db),
                          _: User = Depends(get_current_user)):
    return db.query(Assignment).all()


@assignmentsRouter.post("/assignments", status_code=status.HTTP_201_CREATED)
async def create_assignment(request: AssignmentValidator, db: Session = Depends(get_db),
                            user: User = Depends(get_current_user)):
    request.division = db.query(Division).filter_by(name=request.division).first()
    if request.division:
        new_assignment = Assignment(**request.model_dump(), creator=user)
        db.add(new_assignment)
        db.commit()
        return {"msg": "assignment created"}
    raise HTTPException(status.HTTP_404_NOT_FOUND, "division not found")


@assignmentsRouter.put("/assignments")
async def update_assignment(request: AssignmentValidator, db: Session = Depends(get_db),
                            _: User = Depends(get_current_user)):
    assignment = db.query(Assignment).filter_by(id=request.id).first()
    if assignment:
        request.division = db.query(Division).filter_by(name=request.division).first()
        if request.division:
            assignment.update(**request.model_dump(exclude={"id"}))
            db.commit()
            return {"msg": "updates saved"}
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="division not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="assignment not found")


@assignmentsRouter.delete("/assignments")
async def delete_assignment(assignment_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    assignment = db.query(Assignment).filter_by(id=assignment_id).first()
    if assignment:
        db.delete(assignment)
        db.commit()
        return {"msg": "assignment deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="assignment not found")
