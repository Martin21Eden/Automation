import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


CHROME_NAME = "Chrome"
DEFAULT_CHROME_LOCATION = os.path.join(os.path.dirname(__file__), "chromedriver")


class ChromeDriver:

    def __new__(cls, driver_path: str = DEFAULT_CHROME_LOCATION, *args, **kwargs):
        cls.driver_path = driver_path
        cls.chrome_options = Options()

        return webdriver.Chrome(cls.driver_path, options=cls.chrome_options)


class WebDriver:

    def __init__(self, browser_name: str = CHROME_NAME):
        self.browser = Browser(browser_name)

    def start(self, url):
        self.browser.start_driver()
        self.browser.driver.get(url)
        self.browser.driver.maximize_window()

    @property
    def driver(self) -> webdriver:
        return self.browser.driver

    def quit(self):
        self.browser.driver.quit()


class Browser:

    def __init__(self, browser_name: str):
        self.browser_name = browser_name
        self._driver: webdriver = None

    @property
    def driver(self) -> webdriver:
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    def start_driver(self):
        start_driver_command = {
            CHROME_NAME: self.start_chrome,
        }
        start_driver_command[self.browser_name]()

    def start_chrome(self):
        self.driver = ChromeDriver()
