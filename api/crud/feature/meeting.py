from .feature_base import FeatureBase
from ...db.models.meeting_model import MeetingModel


class Meeting(FeatureBase):
    db_model = MeetingModel
