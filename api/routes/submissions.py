from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from api.const import Permissions
from api.crud.sub_feature.submission import Submission
from api.db.models import UserModel, AssignmentModel  # unresolved reference ignored
from api.dependencies import get_db, CheckPermission
from api.validators import SubmissionValidator, SubmissionUpdateValidator  # unresolved reference ignored

submissionsRouter = APIRouter(
    tags=["Submissions"]
)


@submissionsRouter.get("/submissions")
async def get_submissions(db: Session = Depends(get_db)):
    return Submission.get_db_dump(db)


@submissionsRouter.post("/submissions")
async def create_submission(request: SubmissionValidator, db: Session = Depends(get_db),
                            user: UserModel = Depends(CheckPermission(Permissions.CREATE_SUBMISSION))):
    return Submission.create(request, db, user, "assignment", AssignmentModel)


@submissionsRouter.put("/submissions/{submission_id}")
async def update_submission(submission_id: int, request: SubmissionUpdateValidator, db: Session = Depends(get_db),
                            _: UserModel = Depends(CheckPermission(Permissions.UPDATE_SUBMISSION))):
    return Submission.update(submission_id, db, **request.model_dump())


@submissionsRouter.delete("/submissions/{model_id}")
async def delete_submission(model_id: int, db: Session = Depends(get_db),
                            _: UserModel = Depends(CheckPermission(Permissions.DELETE_SUBMISSION, delete=True,
                                                                   model=Submission.db_model))):
    return Submission.delete(model_id, db)
