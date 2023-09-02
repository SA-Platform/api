from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.models.core_models import UserModel
from api.dependencies import get_db, get_current_user
from api.routers.features_base import Announcement
from api.validators import AnnouncementValidator

announcementsRouter = Announcement.router


@announcementsRouter.get(Announcement.path)
async def get_announcements(db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Announcement.get_db_dump(db)


@announcementsRouter.post(Announcement.path)
async def post_announcement(request: AnnouncementValidator, db: Session = Depends(get_db),
                            user: UserModel = Depends(get_current_user)):
    return Announcement.create(request, db, user)


@announcementsRouter.put(Announcement.path)
async def update_announcement(request: AnnouncementValidator, db: Session = Depends(get_db),
                              _: UserModel = Depends(get_current_user)):
    return Announcement.update(request, db)


@announcementsRouter.delete(Announcement.path)
async def delete_announcement(announcement_id: int, db: Session = Depends(get_db),
                              _: UserModel = Depends(get_current_user)):
    return Announcement.delete(announcement_id, db)
