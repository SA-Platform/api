from .sub_feature_base import SubFeatureBase
from ...db.models import SubmissionModel


class Submission(SubFeatureBase):
    db_model = SubmissionModel
