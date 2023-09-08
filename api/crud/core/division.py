from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .core_base import CoreBase
from ...db.models import DivisionModel
from ...validators import DivisionValidator


class Division(CoreBase):
    validator = DivisionValidator
    db_model = DivisionModel

    @classmethod
    def _check_unique_division(cls, division: DivisionModel, parent: DivisionModel) -> None:
        if division.parent == parent:
            raise HTTPException(status.HTTP_409_CONFLICT,
                                detail=f"division {division.name} with the same parent {parent.name} already exists")

    @classmethod
    def _check_root_division(cls, division: DivisionModel, division_id: int, db: Session) -> None:
        root = cls.get_db_first(db, "parent", None)
        if root and root.id != division_id:
            raise HTTPException(status.HTTP_409_CONFLICT,
                                detail=f"only one root division is allowed, which is {root.name}")

    @classmethod
    def check_division_validity(cls, request: DivisionValidator, db: Session, division_id: int | None = None) -> None:
        division = cls.get_db_first(db, "name", request.name)
        parent = cls.get_db_first(db, "name", request.parent) if request.parent else None

        if request.name == request.parent:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="division can't be its own parent")

        if request.parent:
            if not parent:
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail="parent division doesn't exist")

            if division:
                cls._check_unique_division(division, parent)

                if not division.parent:
                    raise HTTPException(status.HTTP_409_CONFLICT,
                                        detail=f"division {division.name} is a root division and can't have a parent")
        else:
            if division:
                raise HTTPException(status.HTTP_409_CONFLICT, detail=f"division {division.name} already exists")
            else:
                cls._check_root_division(division, division_id, db)
