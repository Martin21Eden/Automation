import pytest
from selenium import webdriver
from .base import Base

driver_state = None
page_stage = None


@pytest.yield_fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    driver.get('https://ec2-54-229-242-35.eu-west-1.compute.amazonaws.com')
    global driver_state
    if not driver_state:
        driver_state = driver
    yield driver
    driver.quit()


@pytest.yield_fixture(scope="function")
def login(driver):
    page = Base(driver)
    global page_stage
    if not page_stage:
        page_stage = page
    page.login('automation@explorium.ai', 'ThisIsATest1!')
    yield page


@pytest.yield_fixture(scope="function", autouse=True)
def del_project():
    yield
    page_stage.delete_project(page_stage.project_name)
