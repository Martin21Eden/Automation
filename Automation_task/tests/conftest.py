import pytest

from Automation_task.webdriver import web_driver
from .data import test_data


@pytest.yield_fixture()
def driver(request):
    web_driver.start(test_data['url'])
    yield
    web_driver.quit()
