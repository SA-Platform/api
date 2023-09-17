from .sub_feature_base import SubFeatureBase
from ...db.models import ExcuseModel, AssignmentModel


class Excuse(SubFeatureBase):
    parent_name = "assignment"
    parent_model = AssignmentModel
    db_model = ExcuseModel
