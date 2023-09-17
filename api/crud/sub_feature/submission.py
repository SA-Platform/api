from .sub_feature_base import SubFeatureBase
from ...db.models import SubmissionModel, AssignmentModel


class Submission(SubFeatureBase):
    parent_name = "assignment"
    parent_model = AssignmentModel
    db_model = SubmissionModel
