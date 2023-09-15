from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from api.crud.core.division import Division
from api.db.models import UserModel, DivisionModel  # unresolved reference ignored
from api.dependencies import get_current_user, get_db
from api.validators import DivisionValidator, DivisionUpdateValidator

divisionsRouter = APIRouter(
    tags=["Divisions"]
)


@divisionsRouter.get("/divisions")
async def get_divisions(db: Session = Depends(get_db),
                        _: UserModel = Depends(get_current_user)):
    return Division.get_db_dump(db)


@divisionsRouter.post("/divisions", status_code=status.HTTP_201_CREATED)
async def create_division(request: DivisionValidator, db: Session = Depends(get_db),
                          _: UserModel = Depends(get_current_user)):
    request.parent = request.parent.lower() if request.parent else None
    request.name = request.name.lower()
    Division.check_division_validity(db, request)
    return Division.create(db, name=request.name, parent=db.query(DivisionModel).filter_by(name=request.parent).first())


@divisionsRouter.put("/divisions/{division_id}")
async def update_division(division_id: int, request: DivisionUpdateValidator, db: Session = Depends(get_db),
                          _: UserModel = Depends(get_current_user)):
    division = db.query(DivisionModel).filter_by(id=division_id).first()  # fetch division to be edited
    if division:
        request.parent = request.parent.lower() if request.parent else None
        request.name = request.name.lower()
        Division.check_division_validity(db, request, division_id)
        division.name = request.name  # set its name
        division.parent = db.query(DivisionModel).filter_by(name=request.parent).first()  # set its parent
        db.commit()
        db.refresh(division)
        return {"msg": "updates saved"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="division not found")


@divisionsRouter.delete("/divisions/{division_id}")
async def delete_division(division_id: int, db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Division.delete(division_id, db)
