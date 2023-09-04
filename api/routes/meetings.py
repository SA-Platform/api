from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.db.models import UserModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user
from api.routes.features_base import Meeting

meetingsRouter = APIRouter(
    tags=["Meetings"]
)


@meetingsRouter.get("/meetings")
async def get_meetings(db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Meeting.get_db_dump(db)


@meetingsRouter.post("/meetings")
async def post_meeting(request: Meeting.validator, db: Session = Depends(get_db),
                       user: UserModel = Depends(get_current_user)):
    return Meeting.create(request, db, user)


@meetingsRouter.put("/meetings/{meeting_id}")
async def put_meeting(meeting_id: int, request: Meeting.validator, db: Session = Depends(get_db),
                      _: UserModel = Depends(get_current_user)):
    return Meeting.update(meeting_id, request, db)


@meetingsRouter.delete("/meetings/{meeting_id}")
async def delete_meeting(meeting_id: int, db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Meeting.delete(meeting_id, db)
