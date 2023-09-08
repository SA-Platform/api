from .feature_base import FeatureBase
from ...db.models import AssignmentModel
from ...validators import AssignmentValidator


class Assignment(FeatureBase):
    validator = AssignmentValidator
    db_model = AssignmentModel
