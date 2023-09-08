from .feature_base import FeatureBase
from ...db.models import MeetingModel
from ...validators import MeetingValidator


class Meeting(FeatureBase):
    validator = MeetingValidator
    db_model = MeetingModel
