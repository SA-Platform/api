from .sub_feature_base import SubFeatureBase
from ...db.models import ExcuseModel


class Excuse(SubFeatureBase):
    db_model = ExcuseModel
