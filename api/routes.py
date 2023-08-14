from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.validators import UserSignup, AnnouncementValidator
from api.db.models import User, Announcement
from api.utils import get_db, create_token, get_current_user

app: FastAPI = FastAPI()


@app.post("/signup", tags=["Users"], status_code=status.HTTP_201_CREATED)
async def signup(request: UserSignup, db: Session = Depends(get_db)):
    new_user: User = User(**request.model_dump())
    db.add(new_user)
    db.commit()
    return {"access_token": create_token({"username": new_user.username}), "token_type": "bearer"}


@app.post("/signin", tags=["Users"], status_code=status.HTTP_200_OK)
async def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: User | None = db.query(User).filter(
        (User.email == form_data.username) | (User.username == form_data.username)).first()
    if user:
        if user.check_password(form_data.password):
            return {"access_token": create_token({"username": user.username}), "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect password")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="user not found")  # for debugging only, should be changed to raise unauthorized always


@app.get("/getusers", tags=["Users"], status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(User).all()


####################### Annauncement endpoints###############################

@app.get("/announcements", tags=["Announcements"], status_code=status.HTTP_200_OK)
async def get_announcements(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Announcement).all()


@app.post("/announcements", tags=["Announcements"], status_code=status.HTTP_201_CREATED)
async def post_announcement(request: AnnouncementValidator, db: Session = Depends(get_db),
                            _: User = Depends(get_current_user)):
    new_Announcement: Announcement = Announcement(**request.model_dump())
    db.add(new_Announcement)
    db.commit()
    return new_Announcement


@app.put("/announcements", tags=["Announcements"], status_code=status.HTTP_200_OK)
async def update_announcement(request: AnnouncementValidator, db: Session = Depends(get_db),
                              _: User = Depends(get_current_user)):
    announcement = db.query(Announcement).filter(Announcement.id == request.announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found")
    announcement.content = request.new_content
    db.commit()
    db.refresh(announcement)
    return announcement


@app.delete("/announcements", tags=["Announcements"], status_code=status.HTTP_200_OK)
async def delete_announcement(announcement_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found")
    db.delete(announcement)
    db.commit()

########################################################################
