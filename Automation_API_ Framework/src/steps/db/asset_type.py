from src.steps.db.base import BaseDbSteps
from src.steps.db.models.asset_type import AssetType


class AssetTypeDbSteps(BaseDbSteps):
    model = AssetType
    name = "asset_type"
