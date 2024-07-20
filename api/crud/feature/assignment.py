from .feature_base import FeatureBase
from ...db.models.assignment_model import AssignmentModel


class Assignment(FeatureBase):
    db_model = AssignmentModel
