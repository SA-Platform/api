from .feature_base import FeatureBase
from ...db.models import AnnouncementModel
from ...validators import AnnouncementValidator


class Announcement(FeatureBase):
    validator = AnnouncementValidator
    db_model = AnnouncementModel
