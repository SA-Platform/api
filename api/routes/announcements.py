from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.const import FeaturePermissions
from api.crud.feature.announcement import Announcement
from api.db.models import UserModel  # unresolved reference ignored
from api.validators import AnnouncementValidator, AnnouncementUpdateValidator
from api.dependencies import get_db, get_current_user, CheckPermission

announcementsRouter = APIRouter(
    tags=["Announcements"]
)


@announcementsRouter.get("/announcements")
async def get_announcements(db: Session = Depends(get_db)):
    return Announcement.get_db_dump(db)


@announcementsRouter.post("/announcements/{division_id}")
async def post_announcement(division_id: int, request: AnnouncementValidator, db: Session = Depends(get_db),
                            user: UserModel = Depends(get_current_user)):
    return Announcement.create(request, db, user)


@announcementsRouter.put("/announcements/{announcement_id}")
async def update_announcement(announcement_id: int, request: AnnouncementUpdateValidator,
                              db: Session = Depends(get_db),
                              user: UserModel = Depends(get_current_user)):
    return Announcement.update(announcement_id, request, db, user)


@announcementsRouter.delete("/announcements/{announcement_id}")
async def delete_announcement(model_id: int, db: Session = Depends(get_db),
                              user: UserModel = Depends(get_current_user)):
    return Announcement.delete(model_id, db, user)
