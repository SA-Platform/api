from .sub_feature_base import SubFeatureBase
from ...db.models import ExcuseModel
from ...validators import ExcuseValidator


class Excuse(SubFeatureBase):
    validator = ExcuseValidator
    db_model = ExcuseModel
