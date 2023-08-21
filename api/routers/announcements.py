from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.db.models import User, Announcement
from api.dependencies import get_db, get_current_user
from api.validators import AnnouncementValidator

announcementsRouter: APIRouter = APIRouter(
    tags=["Announcements"]
)


@announcementsRouter.get("/announcements")
async def get_announcements(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Announcement).all()


@announcementsRouter.post("/announcements")
async def post_announcement(request: AnnouncementValidator, db: Session = Depends(get_db),
                            _: User = Depends(get_current_user)):
    new_announcement: Announcement = Announcement(**request.model_dump())
    db.add(new_announcement)
    db.commit()
    return new_announcement


@announcementsRouter.put("/announcements")
async def update_announcement(request: AnnouncementValidator, db: Session = Depends(get_db),
                              _: User = Depends(get_current_user)):
    announcement = db.query(Announcement).filter_by(id=request.id).first()
    if not announcement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found")
    announcement = Announcement(**request.model_dump())
    db.commit()
    db.refresh(announcement)
    return announcement


@announcementsRouter.delete("/announcements")
async def delete_announcement(announcement_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    announcement = db.query(Announcement).filter_by(id=announcement_id).first()
    if announcement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found")
    db.delete(announcement)
    db.commit()