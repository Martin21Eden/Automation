from src.schemes.asset_type import AssetTypeSchema
from src.steps.api.base import Base
from src.steps.api.models import Meta


class Main(Base):
    meta = Meta(path='/', response_schema=AssetTypeSchema)
