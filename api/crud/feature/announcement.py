from .feature_base import FeatureBase
from ...db.models import AnnouncementModel


class Announcement(FeatureBase):
    db_model = AnnouncementModel
