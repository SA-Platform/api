from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.crud.feature.meeting import Meeting
from api.db.models import UserModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user
from api.validators import MeetingValidator, MeetingUpdateValidator

meetingsRouter = APIRouter(
    tags=["Meetings"]
)


@meetingsRouter.get("/meetings")
async def get_meetings(db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Meeting.get_db_dump(db)


@meetingsRouter.post("/meetings")
async def post_meeting(request: MeetingValidator, db: Session = Depends(get_db),
                       user: UserModel = Depends(get_current_user)):
    return Meeting.create(request, db, user)


@meetingsRouter.put("/meetings/{meeting_id}")
async def update_meeting(meeting_id: int, request: MeetingUpdateValidator, db: Session = Depends(get_db),
                         user: UserModel = Depends(get_current_user)):
    return Meeting.update(meeting_id, request, db, user)


@meetingsRouter.delete("/meetings/{model_id}")
async def delete_meeting(model_id: int,
                         db: Session = Depends(get_db),
                         user: UserModel = Depends(get_current_user)):
    return Meeting.delete(model_id, db, user)
