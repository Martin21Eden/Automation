from http import HTTPStatus

from src.schemes.asset_type import AssetTypeSchema
from src.steps.api.base import Base
from src.steps.api.models import Meta
from src.utils.urls import login


class Login(Base):
    meta = Meta(path=login, response_schema=AssetTypeSchema)

    def post(self, expected_status_code=HTTPStatus.OK, *args, **kwargs):
        return super(Login, self).post(expected_status_code=expected_status_code, *args, **kwargs)
