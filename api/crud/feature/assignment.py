from .feature_base import FeatureBase
from ...db.models import AssignmentModel


class Assignment(FeatureBase):
    db_model = AssignmentModel
