from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.crud.sub_feature.feedback import Feedback
from api.db.models import UserModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user
from api.validators import FeedbackValidator, FeedbackUpdateValidator

feedbacksRouter = APIRouter(
    tags=["Feedback"]
)


@feedbacksRouter.get("/feedback")
async def get_feedback(db: Session = Depends(get_db)):
    return Feedback.get_db_dump(db)


@feedbacksRouter.post("/feedback")
async def create_feedback(request: FeedbackValidator, db: Session = Depends(get_db),
                          user: UserModel = Depends(get_current_user)):
    return Feedback.create(request, db, user)


@feedbacksRouter.put("/feedback/{feedback_id}")
async def update_feedback(feedback_id: int, request: FeedbackUpdateValidator, db: Session = Depends(get_db),
                          user: UserModel = Depends(get_current_user)):
    return Feedback.update(feedback_id, db, user, **request.model_dump())


@feedbacksRouter.delete("/feedback/{model_id}")
async def delete_feedback(model_id: int, db: Session = Depends(get_db),
                          user: UserModel = Depends(get_current_user)):
    return Feedback.delete(model_id, db, user)
