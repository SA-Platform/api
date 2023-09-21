from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.const import FeaturePermissions
from api.crud.sub_feature.feedback import Feedback
from api.db.models import UserModel, SubmissionModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user, CheckPermission
from api.validators import FeedbackValidator, FeedbackUpdateValidator

feedbacksRouter = APIRouter(
    tags=["Feedback"]
)


@feedbacksRouter.get("/feedback")
async def get_feedback(db: Session = Depends(get_db)):
    return Feedback.get_db_dump(db)


@feedbacksRouter.post("/feedback/{division_id}")
async def create_feedback(request: FeedbackValidator, division_id: int, db: Session = Depends(get_db),
                          user: UserModel = Depends(CheckPermission(FeaturePermissions.CREATE_FEEDBACK))):
    return Feedback.create(request, db, user, "submission", SubmissionModel)


@feedbacksRouter.put("/feedback/{feedback_id}")
async def update_feedback(feedback_id: int, division_id: int, request: FeedbackUpdateValidator,
                          db: Session = Depends(get_db),
                          user: UserModel = Depends(CheckPermission(FeaturePermissions.CREATE_FEEDBACK))):
    return Feedback.update(feedback_id, request, db, division_id, user)


@feedbacksRouter.delete("/feedback/{feedback_id}")
async def delete_feedback(feedback_id: int, division_id: int, db: Session = Depends(get_db),
                          user: UserModel = Depends(get_current_user)):
    return Feedback.delete(feedback_id, db, user)
