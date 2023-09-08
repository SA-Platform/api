from .sub_feature_base import SubFeatureBase
from ...db.models import FeedbackModel
from ...validators import FeedbackValidator


class Feedback(SubFeatureBase):
    validator = FeedbackValidator
    db_model = FeedbackModel