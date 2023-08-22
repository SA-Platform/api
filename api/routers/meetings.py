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
                       current_user: User = Depends(get_current_user)):
    new_meeting_data = request.model_dump()
    division_name = new_meeting_data.pop('division')
    division = db.query(Division).filter(Division.name == division_name).first()
    if not division:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Division not found")
    new_meeting_data['division_id'] = division.id
    new_meeting_data['creator_id'] = current_user.id
    new_meeting = Meeting(**new_meeting_data)
    db.add(new_meeting)
    db.commit()
    return new_meeting


@meetingsRouter.put("/meetings")
async def put_meeting(request: MeetingValidator, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    if request.id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="did not provide meeting id")
    existing_meeting = db.query(Meeting).filter(Meeting.id == request.id).first()

    if not existing_meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")

    updated_meeting_data = request.model_dump(exclude_unset=True)

    division_name = updated_meeting_data.pop('division')
    division = db.query(Division).filter(Division.name == division_name).first()
    if not division:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Division not found")

    updated_meeting_data['division_id'] = division.id
    existing_meeting.date = updated_meeting_data.pop('date')
    existing_meeting.location_text = updated_meeting_data.pop('location_text')
    existing_meeting.location_lat = updated_meeting_data.pop('location_lat')
    existing_meeting.location_long = updated_meeting_data.pop('location_long')
    existing_meeting.title = updated_meeting_data.pop('title')
    existing_meeting.description = updated_meeting_data.pop('description')

    db.commit()
    return existing_meeting


@meetingsRouter.delete("/meetings")
async def delete_meeting(meeting_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    meeting = db.query(Meeting).filter_by(id=meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    db.delete(meeting)
    db.commit()
    return meeting
