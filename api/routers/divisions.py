from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.validators import DivisionValidator
from api.db.models.core_models import UserModel, DivisionModel

divisionsRouter: APIRouter = APIRouter(
    tags=["Division"]
)


@divisionsRouter.get("/divisions", )
async def get_divisions(db: Session = Depends(get_db),
                        _: UserModel = Depends(get_current_user)):
    return db.query(DivisionModel).all()


@divisionsRouter.post("/divisions", status_code=status.HTTP_201_CREATED)
async def create_division(request: DivisionValidator, db: Session = Depends(get_db),
                          _: UserModel = Depends(get_current_user)):
    new_division: DivisionModel = DivisionModel(name=request.name,
                                      parent=db.query(DivisionModel).filter_by(name=request.parent).first())
    db.add(new_division)
    db.commit()
    return new_division


@divisionsRouter.put("/divisions")
async def update_division(request: DivisionValidator, db: Session = Depends(get_db),
                          _: UserModel = Depends(get_current_user)):
    division = db.query(DivisionModel).filter_by(id=request.id).first()  # fetch division to be edited
    if division:
        division.name = request.name  # set its name
        division.parent = db.query(DivisionModel).filter_by(name=request.parent).first()  # set its parent
        db.commit()
        db.refresh(division)
        return {"msg": "updates saved"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="division not found")


@divisionsRouter.delete("/divisions")
async def delete_division(division_id: int, db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    division = db.query(DivisionModel).filter_by(id=division_id).first()
    if division:
        db.delete(division)
        db.commit()
        return {"message": "division deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="division not found")
