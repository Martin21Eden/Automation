from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os, random


class PageElement(object):
    def __init__(self, locator, time_out=15):
        self.time_out = time_out
        self.locator = locator

    def __get__(self, instance, owner):
        return WebDriverWait(instance.driver, self.time_out, poll_frequency=0.1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.locator)))

    def __set__(self, instance, value):
        elem = self.__get__(instance, instance.__class__)
        if not elem:
            raise ValueError("Can't set value, element not found")
        elem.clear()
        elem.send_keys(value)


class PageElements(object):
    def __init__(self, locator, time_out=15):
        self.time_out = time_out
        self.locator = locator

    def __get__(self, instance, owner):
        return WebDriverWait(instance.driver, self.time_out, poll_frequency=0.1).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.locator)))

    def __set__(self, instance, value):
        elems = self.__get__(instance, instance.__class__)
        if not elems:
            raise ValueError("Can't set value, no elements found")
        [elem.send_keys(value) for elem in elems]


class Base(object):
    user_email = PageElement('#user-email')
    user_password = PageElement('#user-password')
    submit_form = PageElement('#submit-form')
    create_button = PageElement('#main-content > div > div > div > div:nth-child(1) > div.btn')
    projectNameInput = PageElement('#projectNameInput')
    createProjectButton = PageElement('#createProjectButton')
    projects = PageElements('#main-content > div > div > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(2) > div.project-list > div > div > div > div.project-name.ng-binding')
    popup_project = PageElement('#dataset-details > div > div > div > div:nth-child(1) > div.ng-isolate-scope > div')
    logo = PageElement('#homeLink')
    menu = PageElements('#main-content > div > div > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(2) > div.project-list > div > div > div div:nth-child(2)')
    del_button = PageElement('#deleteProject')

    @staticmethod
    def wait(time):
        __import__('time').sleep(time)

    def __init__(self, driver):
        self.driver = driver
        self.project_name = f'Project_{random.randint(0, 100)}'

    def login(self, email, password):
        self.user_email = email
        self.user_password = password
        self.submit_form.click()

    def find_project(self, project_name):
        [project.click() for project in self.projects if project.text == project_name]

    def upload_file_to_project(self):
        self.refresh_page()
        self.wait(5)
        self.driver.find_element_by_css_selector('body > input').send_keys(
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'document.csv')))

    def create_project(self):
        self.create_button.click()
        self.projectNameInput = self.project_name
        self.createProjectButton.click()
        self.refresh_page()

    def refresh_page(self):
        self.driver.refresh()

    @property
    def uploaded_file(self)->bool:
        return self.popup_project.is_displayed()

    def delete_project(self, project_name):
        self.logo.click()
        for num_project, project in enumerate(self.projects):
            if project.text == project_name:
                [item.click() for num, item in enumerate(self.menu) if num == num_project*2]
                self.del_button.click()
                alert = self.driver.switch_to.alert
                alert.accept()
