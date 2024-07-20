from .feature_base import FeatureBase
from ...db.models.announcement_model import AnnouncementModel


class Announcement(FeatureBase):
    db_model = AnnouncementModel
