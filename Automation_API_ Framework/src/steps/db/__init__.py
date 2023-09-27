from src.clients.db import BaseDb
from src.steps.db.asset_type import AssetTypeDbSteps
from src.steps.db.billabe_client_contact import BillableClientContactDbSteps
from src.steps.db.billable_client import BillableClientDbSteps
from src.steps.db.billable_service import BillableService
from src.steps.db.base import Registry
from src.steps.db.sales_order import SalesOrderDbSteps


class _Client(BaseDb):
    def __init__(self, db_url):
        super(_Client, self).__init__(db_url)


class DbSteps:
    def __init__(self, db_url):
        self.db_client = _Client(db_url)
        for cls in list(Registry.REGISTRY.values())[1:]:
            setattr(self, cls.name, cls(self.db_client))
