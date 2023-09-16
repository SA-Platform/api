from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.const import Permissions
from api.crud.feature.announcement import Announcement
from api.db.models import UserModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user, CheckPermission

announcementsRouter = APIRouter(
    tags=["Announcements"]
)


@announcementsRouter.get("/announcements")
async def get_announcements(db: Session = Depends(get_db)):
    return Announcement.get_db_dump(db)


@announcementsRouter.post("/announcements")
async def post_announcement(request: Announcement.validator, db: Session = Depends(get_db),
                            user: UserModel = Depends(CheckPermission(Permissions.CREATE_ANNOUNCEMENT))):
    return Announcement.create(request, db, user)


@announcementsRouter.put("/announcements/{announcement_id}")
async def update_announcement(announcement_id: int, request: Announcement.validator, db: Session = Depends(get_db),
                              _: UserModel = Depends(CheckPermission(Permissions.UPDATE_ANNOUNCEMENT))):
    return Announcement.update(announcement_id, request, db)


@announcementsRouter.delete("/announcements/{model_id}")
async def delete_announcement(model_id: int, db: Session = Depends(get_db),
                              _: UserModel = Depends(CheckPermission(Permissions.DELETE_ANNOUNCEMENT, delete=True,
                                                                     model=Announcement.db_model))):
    return Announcement.delete(model_id, db)
