from .sub_feature_base import SubFeatureBase
from ...db.models import FeedbackModel


class Feedback(SubFeatureBase):
    db_model = FeedbackModel
