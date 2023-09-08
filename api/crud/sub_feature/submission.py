from .sub_feature_base import SubFeatureBase
from ...db.models import SubmissionModel
from ...validators import SubmissionValidator


class Submission(SubFeatureBase):
    validator = SubmissionValidator
    db_model = SubmissionModel
