from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.const import Permissions
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


@feedbacksRouter.post("/feedback")
async def create_feedback(request: FeedbackValidator, db: Session = Depends(get_db),
                          user: UserModel = Depends(CheckPermission(Permissions.CREATE_FEEDBACK))):
    return Feedback.create(request, db, user, "submission", SubmissionModel)


@feedbacksRouter.put("/feedback/{feedback_id}")
async def update_feedback(feedback_id: int, request: FeedbackUpdateValidator, db: Session = Depends(get_db),
                          _: UserModel = Depends(CheckPermission(Permissions.UPDATE_FEEDBACK))):
    return Feedback.update(feedback_id, db,  **request.model_dump())


@feedbacksRouter.delete("/feedback/{model_id}")
async def delete_feedback(model_id: int, db: Session = Depends(get_db),
                          _: UserModel = Depends(CheckPermission(Permissions.DELETE_FEEDBACK, delete=True,
                                                                 model=Feedback.db_model))):
    return Feedback.delete(model_id, db)
