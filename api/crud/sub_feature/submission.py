from .sub_feature_base import SubFeatureBase
from ...db.models.submission_model import SubmissionModel
from ...db.models.assignment_model import AssignmentModel



class Submission(SubFeatureBase):
    parent_name = "assignment"
    parent_model = AssignmentModel
    db_model = SubmissionModel
