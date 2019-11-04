import pytest

from Automation_task.webdriver import web_driver
from .config import url


@pytest.yield_fixture()
def driver(request):
    web_driver.start(url)
    yield
    web_driver.quit()
