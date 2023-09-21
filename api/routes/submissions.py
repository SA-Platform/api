from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.const import FeaturePermissions
from api.crud.sub_feature.submission import Submission
from api.db.models import UserModel  # unresolved reference ignored
from api.db.models.assignment_model import AssignmentModel
from api.dependencies import get_db, get_current_user, CheckPermission
from api.validators import SubmissionValidator, SubmissionUpdateValidator  # unresolved reference ignored

submissionsRouter = APIRouter(
    tags=["Submissions"]
)


@submissionsRouter.get("/submissions")
async def get_submissions(db: Session = Depends(get_db)):
    return Submission.get_db_dump(db)


@submissionsRouter.post("/submissions/{division_id}")
async def create_submission(request: SubmissionValidator, division_id: int,
                            db: Session = Depends(get_db),
                            user: UserModel = Depends(CheckPermission(FeaturePermissions.CREATE_SUBMISSION))):
    return Submission.create(request, db, user, "assignment", AssignmentModel)


@submissionsRouter.put("/submissions/{submission_id}/{division_id}")
async def update_submission(submission_id: int, division_id: int, request: SubmissionUpdateValidator,
                            db: Session = Depends(get_db),
                            user: UserModel = Depends(CheckPermission(FeaturePermissions.UPDATE_SUBMISSION))):
    return Submission.update(submission_id, request, db, division_id, user)


@submissionsRouter.delete("/submissions/{submission_id}/{division_id}")
async def delete_submission(submission_id: int, division_id: int,
                            db: Session = Depends(get_db),
                            user: UserModel = Depends(CheckPermission(FeaturePermissions.DELETE_SUBMISSION))):
    return Submission.delete(submission_id, db, user)
