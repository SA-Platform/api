from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.db.models import User, Meeting, Division
from api.dependencies import get_db, get_current_user
from api.validators import MeetingValidator

meetingsRouter: APIRouter = APIRouter(
    tags=["Meetings"]
)


@meetingsRouter.get("/meetings")
async def get_meetings(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Meeting).all()


@meetingsRouter.post("/meetings")
async def post_meeting(request: MeetingValidator, db: Session = Depends(get_db),
                       user: User = Depends(get_current_user)):
    request.division = db.query(Division).filter_by(name=request.division).first()
    if request.division:
        new_meeting = Meeting(**request.model_dump(), creator=user)
        db.add(new_meeting)
        db.commit()
        return {"msg": "meeting created"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="division not found")


@meetingsRouter.put("/meetings")
async def put_meeting(request: MeetingValidator, db: Session = Depends(get_db),
                      _: User = Depends(get_current_user)):
    meeting = db.query(Meeting).filter_by(id=request.id).first()
    if meeting:
        request.division = db.query(Division).filter_by(name=request.division).first()
        if request.division:
            meeting.update(**request.model_dump(exclude={"id"}))
            db.commit()
            return {"msg": "updates saved"}
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="division not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="meeting not found")


@meetingsRouter.delete("/meetings")
async def delete_meeting(meeting_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    meeting = db.query(Meeting).filter_by(id=meeting_id).first()
    if meeting:
        db.delete(meeting)
        db.commit()
        return {"msg": "meeting deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="meeting not found")
