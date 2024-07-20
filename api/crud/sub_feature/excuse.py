from .sub_feature_base import SubFeatureBase
from ...db.models.excuse_model import ExcuseModel
from ...db.models.assignment_model import AssignmentModel


class Excuse(SubFeatureBase):
    parent_name = "assignment"
    parent_model = AssignmentModel
    db_model = ExcuseModel
