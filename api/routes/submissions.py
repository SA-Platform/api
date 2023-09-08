from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.db.models import UserModel, AssignmentModel  # unresolved reference ignored
from api.dependencies import get_db, get_current_user
from api.routes.features_base import Submission
from api.validators import SubmissionValidator, SubmissionBaseValidator # unresolved reference ignored

submissionsRouter = APIRouter(
    tags=["Submissions"]
)


@submissionsRouter.get("/submissions")
async def get_submissions(db: Session = Depends(get_db), _: UserModel = Depends(get_current_user)):
    return Submission.get_db_dump(db)


@submissionsRouter.post("/submissions")
async def create_submission(request: SubmissionValidator, db: Session = Depends(get_db),
                            user: UserModel = Depends(get_current_user)):
    return Submission.create(request, db, user, "assignment", AssignmentModel)


@submissionsRouter.put("/submissions/{submission_id}")
async def update_submission(submission_id: int, request: SubmissionBaseValidator, db: Session = Depends(get_db),
                            _: UserModel = Depends(get_current_user)):
    return Submission.update(submission_id, request, db)


@submissionsRouter.delete("/submissions/{submission_id}")
async def delete_submission(submission_id: int, db: Session = Depends(get_db),
                            _: UserModel = Depends(get_current_user)):
    return Submission.delete(submission_id, db)
