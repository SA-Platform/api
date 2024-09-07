from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from api.const import CorePermissions
from api.crud.core.division import Division
from api.db.models import UserModel
from api.db.models import DivisionModel
from api.dependencies import get_db, CheckPermission
from api.validators.division_validator import DivisionValidator, DivisionUpdateValidator

divisionsRouter = APIRouter(tags=["Divisions"])


@divisionsRouter.get("/divisions")
async def get_divisions(db: Session = Depends(get_db)):
    return Division.get_db_dump(db)


@divisionsRouter.post("/divisions", status_code=status.HTTP_201_CREATED)
async def create_division(
    request: DivisionValidator,
    db: Session = Depends(get_db),
    _: UserModel = Depends(CheckPermission(CorePermissions.CREATE_DIVISION, core=True)),
):
    request.name = request.name.strip().lower()
    request.parent = request.parent.strip().lower() if request.parent else None
    Division.check_division_validity(db, request)
    return Division.create(
        db,
        name=request.name,
        parent=db.query(DivisionModel).filter_by(name=request.parent).first(),
    )


@divisionsRouter.put("/divisions/{division_id}")
async def update_division(
    division_id: int,
    request: DivisionUpdateValidator,
    db: Session = Depends(get_db),
    _: UserModel = Depends(CheckPermission(CorePermissions.UPDATE_DIVISION, core=True)),
):
    division = (
        db.query(DivisionModel).filter_by(id=division_id).first()
    )  # fetch division to be edited
    if division:
        Division.check_division_validity(db, request, division_id)
        division.name = request.name  # set its name
        division.parent = (
            db.query(DivisionModel).filter_by(name=request.parent).first()
        )  # set its parent
        db.commit()
        db.refresh(division)
        return {"msg": "updates saved"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="division not found"
    )


@divisionsRouter.delete("/divisions/{division_id}")
async def delete_division(
    division_id: int,
    db: Session = Depends(get_db),
    _: UserModel = Depends(CheckPermission(CorePermissions.DELETE_DIVISION, core=True)),
):
    return Division.delete(division_id, db)
