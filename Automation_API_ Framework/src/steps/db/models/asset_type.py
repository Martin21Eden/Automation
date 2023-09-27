import sqlalchemy as sa

from src.steps.db.models.base import BaseModel


class AssetType(BaseModel):
    __tablename__ = 'asset_type'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name = sa.Column(sa.VARCHAR(100), nullable=False)
    is_active = sa.Column(sa.Boolean, nullable=False)
    created_at = sa.Column(sa.DateTime)
    updated_at = sa.Column(sa.DateTime)
