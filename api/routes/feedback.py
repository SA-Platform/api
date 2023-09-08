from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.crud.sub_feature.feedback import Feedback
from api.db.models import UserModel, SubmissionModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user
from api.validators import FeedbackValidator, FeedbackBaseValidator

feedbacksRouter = APIRouter(
    tags=["Feedback"]
)


@feedbacksRouter.get("/feedback")
async def get_feedbacks(db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Feedback.get_db_dump(db)


@feedbacksRouter.post("/feedback")
async def create_feedback(request: FeedbackValidator, db: Session = Depends(get_db),
                          user: UserModel = Depends(get_current_user)):
    return Feedback.create(request, db, user, "submission", SubmissionModel)


@feedbacksRouter.put("/feedback/{feedback_id}")
async def update_feedback(feedback_id: int, request: FeedbackBaseValidator, db: Session = Depends(get_db),
                          _: UserModel = Depends(get_current_user)):
    return Feedback.update(feedback_id, db,  **request.model_dump())


@feedbacksRouter.delete("/feedback/{feedback_id}")
async def delete_feedback(feedback_id: int, db: Session = Depends(get_db),
                          _: UserModel = Depends(get_current_user)):
    return Feedback.delete(feedback_id, db)
