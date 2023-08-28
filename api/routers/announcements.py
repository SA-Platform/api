from fastapi import Depends
from sqlalchemy.orm import Session

from api.db.models.core_models import User
from api.db.models.feature_models import Announcement
from api.dependencies import get_db, get_current_user
from api.routers.features_base import Base
from api.validators import AnnouncementValidator

announcementsHandler = Base("announcement", "Announcements", AnnouncementValidator, Announcement)
announcementsRouter = announcementsHandler.router


@announcementsRouter.get(announcementsHandler.path)
async def get_announcements(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return announcementsHandler.get_all(db)


@announcementsRouter.post(announcementsHandler.path)
async def post_announcement(request: AnnouncementValidator, db: Session = Depends(get_db),
                            user: User = Depends(get_current_user)):
    return announcementsHandler.create(request, db, user)


@announcementsRouter.put(announcementsHandler.path)
async def update_announcement(request: AnnouncementValidator, db: Session = Depends(get_db),
                              _: User = Depends(get_current_user)):
    return announcementsHandler.update(request, db)


@announcementsRouter.delete(announcementsHandler.path)
async def delete_announcement(announcement_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return announcementsHandler.delete(announcement_id, db)
