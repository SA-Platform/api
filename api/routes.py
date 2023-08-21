from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session
from api.validators import UserValidator, AnnouncementValidator, DivisionValidator, UsernameValidator
from api.db.models import User, Announcement, Division
from api.utils import get_db, create_token, get_current_user

app: FastAPI = FastAPI()


@app.post("/signup", tags=["Users"], status_code=status.HTTP_201_CREATED)
async def signup(request: UserValidator, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=request.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

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


@app.post("/validate_username", tags=["Users"], status_code=status.HTTP_202_ACCEPTED)
async def validate_username(request: UsernameValidator,
                            db: Session = Depends(get_db)):  ##### need to change the validation error msg
    existing_user = db.query(User).filter_by(username=request.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username is taken")
    return {"message": "username is available"}


# @app.post("/validate_email", tags=["Users"], status_code=status.HTTP_202_ACCEPTED)
# async def validate_email(email: EmailStr, db: Session = Depends(get_db)):
#     existing_user = db.query(User).filter_by(email=email).first()
#     if existing_user:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
#     return {"message": "Email is available"}


@app.get("/announcements", tags=["Announcements"], status_code=status.HTTP_200_OK)
async def get_announcements(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Announcement).all()


@app.post("/announcements", tags=["Announcements"], status_code=status.HTTP_201_CREATED)
async def post_announcement(request: AnnouncementValidator, db: Session = Depends(get_db),
                            _: User = Depends(get_current_user)):
    new_announcement: Announcement = Announcement(**request.model_dump())
    db.add(new_announcement)
    db.commit()
    return new_announcement


@app.put("/announcements", tags=["Announcements"], status_code=status.HTTP_200_OK)
async def update_announcement(request: AnnouncementValidator, db: Session = Depends(get_db),
                              _: User = Depends(get_current_user)):
    announcement = db.query(Announcement).filter_by(id=request.id).first()
    if not announcement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found")
    announcement = Announcement(**request.model_dump())
    db.commit()
    db.refresh(announcement)
    return announcement


@app.delete("/announcements", tags=["Announcements"], status_code=status.HTTP_200_OK)
async def delete_announcement(announcement_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    announcement = db.query(Announcement).filter_by(id=announcement_id).first()
    if announcement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found")
    db.delete(announcement)
    db.commit()


@app.get("/divisions", tags=["Divisions"], status_code=status.HTTP_200_OK)
async def get_divisions(db: Session = Depends(get_db),
                        _: User = Depends(get_current_user)):
    return db.query(Division).all()


@app.post("/divisions", tags=["Divisions"], status_code=status.HTTP_201_CREATED)
async def create_division(request: DivisionValidator, db: Session = Depends(get_db),
                          _: User = Depends(get_current_user)):
    new_division: Division = Division(name=request.name,
                                      parent=db.query(Division).filter_by(name=request.parent).first())
    db.add(new_division)
    db.commit()
    return new_division


@app.put("/divisions", tags=["Divisions"], status_code=status.HTTP_200_OK)
async def update_division(request: DivisionValidator, db: Session = Depends(get_db),
                          _: User = Depends(get_current_user)):
    division = db.query(Division).filter_by(id=request.id).first()  # fetch division to be edited
    division.name = request.name  # set its name
    division.parent = db.query(Division).filter_by(name=request.parent).first()  # set its parent
    db.commit()
    db.refresh(division)
    return division


@app.delete("/divisions", tags=["Divisions"], status_code=status.HTTP_200_OK)
async def delete_division(division_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    division = db.query(Division).filter_by(id=division_id).first()
    if division:
        db.delete(division)
        db.commit()
        return {"message": "division deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="division not found")
