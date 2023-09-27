from src.schemes.asset_type import AssetTypeSchema
from src.steps.api.base import Base, Meta
from src.utils.urls import asset_type


class AssetType(Base):
    meta = Meta(path=asset_type, response_schema=AssetTypeSchema)
