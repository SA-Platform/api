from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.db.models import UserModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user
from api.routers.features_base import Announcement

announcementsRouter = APIRouter(
    tags=["Announcements"]
)


@announcementsRouter.get("/announcements")
async def get_announcements(db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Announcement.get_db_dump(db)


@announcementsRouter.post("/announcements")
async def post_announcement(request: Announcement.validator, db: Session = Depends(get_db),
                            user: UserModel = Depends(get_current_user)):
    return Announcement.create(request, db, user)


@announcementsRouter.put("/announcements/{announcement_id}")
async def update_announcement(announcement_id: int, request: Announcement.validator, db: Session = Depends(get_db),
                              _: UserModel = Depends(get_current_user)):
    return Announcement.update(announcement_id, request, db)


@announcementsRouter.delete("/announcements/{announcement_id}")
async def delete_announcement(announcement_id: int, db: Session = Depends(get_db),
                              _: UserModel = Depends(get_current_user)):
    return Announcement.delete(announcement_id, db)
