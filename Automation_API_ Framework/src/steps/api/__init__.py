from src.steps.api.base import Base
from src.steps.api.service.asset_type import AssetType

from src.steps.api.site.site import Main


class ServiceApiSteps(object):
    def __init__(self, client):
        self.asset_type = AssetType(client)


class SiteApiSteps(object):
    def __init__(self, client):
        self.main = Main(client)
