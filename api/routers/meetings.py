from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.models.core_models import UserModel
from api.dependencies import get_db, get_current_user
from api.routers.features_base import Meeting
from api.validators import MeetingValidator

meetingsRouter = Meeting.router


@meetingsRouter.get(Meeting.path)
async def get_meetings(db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Meeting.get_db_dump(db)


@meetingsRouter.post(Meeting.path)
async def post_meeting(request: MeetingValidator, db: Session = Depends(get_db),
                       user: UserModel = Depends(get_current_user)):
    return Meeting.create(request, db, user)


@meetingsRouter.put(Meeting.path)
async def put_meeting(request: MeetingValidator, db: Session = Depends(get_db),
                      _: UserModel = Depends(get_current_user)):
    return Meeting.update(request, db)


@meetingsRouter.delete(Meeting.path)
async def delete_meeting(meeting_id: int, db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Meeting.delete(meeting_id, db)
