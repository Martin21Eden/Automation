from pytest import fixture

from src.utils.models import Session, AssetType

session_inst = None


@fixture(scope='session')
def create_asset_type(service, session) -> AssetType:

    yield AssetType(service, session)


@fixture(scope='session')
def session(site, request) -> Session:
    global session_inst
    session_inst = Session(site=site)

    yield session_inst
