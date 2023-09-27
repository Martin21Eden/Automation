from pytest import fixture

from src.clients.http import HttpClient

from src.steps.api import ServiceApiSteps, SiteApiSteps
from src.data.data import Data
from src.config import settings

pytest_plugins = ['src.fixtures.common']


@fixture(scope='session')
def env(request):
    yield settings[request.config.getoption("--env")]


@fixture(scope='session')
def data(request):
    yield Data(request.config.getoption("--env"))


@fixture(scope='session')
def service(env):
    client = HttpClient(env.host.service)

    yield ServiceApiSteps(client)


@fixture(scope='session')
def site(env):
    client = HttpClient(env.host.site)

    yield SiteApiSteps(client)



def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="prod/dev")
    parser.addoption("--local", action="store", default=False, help="True/False")
