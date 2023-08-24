from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, Mapper, DeclarativeBase
from starlette import status

from api.db.models import Division


class Base:
    """Base class for all features, contains the basic CRUD operations"""
    name: str
    tag: str
    path: str
    router: APIRouter
    validator: BaseModel
    db_model: DeclarativeBase

    def __init__(self, name, tag, validator, db_model):
        self.name = name
        self.tag = tag
        self.path = f"/{tag.lower()}"
        self.router = APIRouter(tags=[tag])
        self.validator = validator
        self.db_model = db_model

    def get_all(self, db: Session):
        return db.query(self.db_model).all()

    def create(self, request: BaseModel, db: Session, user: Mapper):
        request.division = db.query(Division).filter_by(name=request.division).first()
        if request.division:
            new_model = self.db_model(**request.model_dump(), creator = user)
            db.add(new_model)
            db.commit()
            return {"msg": f"{self.name} created"}
        raise HTTPException(status.HTTP_404_NOT_FOUND, "division not found")

    def update(self, request: BaseModel, db: Session):
        model = db.query(self.db_model).filter_by(id=request.id).first()
        if model:
            request.division = db.query(Division).filter_by(name=request.division).first()
            if request.division:
                model.update(**request.model_dump(exclude={"id"}))
                db.commit()
                return {"msg": "updates saved"}
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="division not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.name} not found")

    def delete(self, model_id: int, db: Session):
        model = db.query(self.db_model).filter_by(id=model_id).first()
        if model:
            db.delete(model)
            db.commit()
            return {"msg": f"{self.name} deleted"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.name} not found")
