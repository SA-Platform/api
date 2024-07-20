from .sub_feature_base import SubFeatureBase
from ...db.models.feedback_model import FeedbackModel
from ...db.models.submission_model import SubmissionModel



class Feedback(SubFeatureBase):
    parent_name = "submission"
    parent_model = SubmissionModel
    db_model = FeedbackModel
