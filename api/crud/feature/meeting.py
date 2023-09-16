from .feature_base import FeatureBase
from ...db.models import MeetingModel


class Meeting(FeatureBase):
    db_model = MeetingModel
