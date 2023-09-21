from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.const import FeaturePermissions
from api.crud.feature.meeting import Meeting
from api.db.models import UserModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user, CheckPermission
from api.validators import MeetingValidator, MeetingUpdateValidator

meetingsRouter = APIRouter(
    tags=["Meetings"]
)


@meetingsRouter.get("/meetings")
async def get_meetings(db: Session = Depends(get_db)):
    return Meeting.get_db_dump(db)


@meetingsRouter.post("/meetings/{division_id}")
async def post_meeting(division_id: int, request: MeetingValidator, db: Session = Depends(get_db),
                       user: UserModel = Depends(CheckPermission(FeaturePermissions.CREATE_MEETING))):
    return Meeting.create(request, db, user, division_id)


@meetingsRouter.put("/meetings/{meeting_id}/{division_id}")
async def update_meeting(meeting_id: int, request: MeetingUpdateValidator, division_id: int,
                         db: Session = Depends(get_db),
                         user: UserModel = Depends(CheckPermission(FeaturePermissions.UPDATE_MEETING))):
    return Meeting.update(meeting_id, request, db, division_id, user)


@meetingsRouter.delete("/meetings/{model_id}/{division_id}")
async def delete_meeting(meeting_id: int,
                         db: Session = Depends(get_db),
                         user: UserModel = Depends(CheckPermission(FeaturePermissions.DELETE_MEETING))):
    return Meeting.delete(meeting_id, db, user)
