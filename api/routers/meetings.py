from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.models.core_models import User
from api.db.models.feature_models import Meeting
from api.dependencies import get_db, get_current_user
from api.routers.features_base import Base
from api.validators import MeetingValidator

meetingsHandler = Base("meeting", "Meetings", MeetingValidator, Meeting)
meetingsRouter = meetingsHandler.router


@meetingsRouter.get(meetingsHandler.path)
async def get_meetings(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return meetingsHandler.get_all(db)


@meetingsRouter.post(meetingsHandler.path)
async def post_meeting(request: MeetingValidator, db: Session = Depends(get_db),
                       user: User = Depends(get_current_user)):
    return meetingsHandler.create(request, db, user)


@meetingsRouter.put(meetingsHandler.path)
async def put_meeting(request: MeetingValidator, db: Session = Depends(get_db),
                      _: User = Depends(get_current_user)):
    return meetingsHandler.update(request, db)


@meetingsRouter.delete(meetingsHandler.path)
async def delete_meeting(meeting_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return meetingsHandler.delete(meeting_id, db)
