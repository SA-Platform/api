from .sub_feature_base import SubFeatureBase
from ...db.models import FeedbackModel, SubmissionModel


class Feedback(SubFeatureBase):
    parent_name = "submission"
    parent_model = SubmissionModel
    db_model = FeedbackModel
