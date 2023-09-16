from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.const import Permissions
from api.crud.feature.meeting import Meeting
from api.db.models import UserModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user, CheckPermission

meetingsRouter = APIRouter(
    tags=["Meetings"]
)


@meetingsRouter.get("/meetings")
async def get_meetings(db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Meeting.get_db_dump(db)


@meetingsRouter.post("/meetings")
async def post_meeting(request: Meeting.validator,
                       db: Session = Depends(get_db),
                       user: UserModel = Depends(CheckPermission(Permissions.CREATE_MEETING))):
    return Meeting.create(request, db, user)


@meetingsRouter.put("/meetings/{meeting_id}")
async def update_meeting(meeting_id: int,
                         request: Meeting.validator,
                         db: Session = Depends(get_db),
                         _: UserModel = Depends(CheckPermission(Permissions.UPDATE_MEETING))):
    return Meeting.update(meeting_id, request, db)


@meetingsRouter.delete("/meetings/{model_id}")
async def delete_meeting(model_id: int,
                         db: Session = Depends(get_db),
                         _: UserModel = Depends(CheckPermission(Permissions.DELETE_MEETING, delete=True,
                                                                model=Meeting.db_model))):
    return Meeting.delete(model_id, db)
