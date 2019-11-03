from typing import Any, Tuple, List, Dict, Optional
import functools
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from Automation_task.webdriver import web_driver

_DEFAULT_TIMEOUT = 30
_TIMEOUT_MESSAGE = 'Could not wait for {} of element. Tried for {} seconds'


def catch_errors(miss: Tuple = ()):
    """
    Decorator to catch unexpected errors.
    By default decorator is enabled. To disable decorator pass to decorated function named argument 'catch=False'
    :param miss: tuple of errors that are desirable to be raised
    """

    def catcher_wrapper(func):
        @functools.wraps(func)
        def catcher(obj, catch=True, *args, **kwargs):
            if catch:
                try:
                    return func(obj, *args, **kwargs)
                except Exception as e:
                    if e.__class__ in miss:
                        raise e
                    print('HANDLING AN EXCEPTION ', e)
                    return False
            else:
                return func(obj, *args, **kwargs)

        return catcher

    return catcher_wrapper


class Element:
    """
    Class contains _common functionality of all types of elements
    """

    def __init__(self, locator: Tuple[By, str] = None, parent: Any = None, web_element: WebElement = None):
        if locator is None and web_element is None:
            raise ValueError('Locator or WebElement must be passed as argument')
        self._locator = locator
        self._parent = parent
        self._web_element = web_element

    @property
    def _driver(self):
        if not hasattr(self, 'driver_obj'):
            driver = web_driver.driver
            if driver is None:
                raise Exception('web_driver.driver is None')
            setattr(self, 'driver_obj', driver)
        return self.__dict__['driver_obj']

    def _wait(self, timeout: int = _DEFAULT_TIMEOUT) -> WebDriverWait:
        return WebDriverWait(self._driver, timeout)

    @property
    def _finder(self) -> Any:
        return self._parent or self._driver

    @property
    def web_element(self) -> WebElement:
        """
        Returns enclosed web element
        :return: WebElement instance
        """
        return self.__wait_web_element_dynamically()

    def __wait_web_element_dynamically(self, timeout=_DEFAULT_TIMEOUT) -> WebElement:
        """
        Waits for web element to be present and visible and returns it
        :param timeout: seconds to wait for element
        :return: WebElement instance
        """
        element = None
        if self._locator:
            self._wait(timeout).until(lambda _: self.is_present(),
                                      message=f'Could not wait for element with locator {self._locator} to be present')
            element = self._finder.find_element(*self._locator)

        elif self._web_element:
            self._wait(timeout).until(ec.visibility_of(self._web_element),
                                      message=f'Could not wait for visibility element {self._web_element.id}')
            element = self._web_element
        self.scroll_into_view(element)
        return element

    def wait_for_visibility(self, message=None, timeout=_DEFAULT_TIMEOUT):
        return self._wait(timeout).until(lambda _: self.is_displayed(),
                                         message=message or _TIMEOUT_MESSAGE.format('visibility', f'{timeout}'))

    def wait_to_be_clickable(self, message=None, timeout=_DEFAULT_TIMEOUT):
        return self._wait(timeout).until(ec.element_to_be_clickable(self._locator),
                                         message=message or _TIMEOUT_MESSAGE.format('clickability', f'{timeout}'))

    def wait_to_be_enabled(self, message=None, timeout=_DEFAULT_TIMEOUT):
        return self._wait(timeout).until(lambda _: self.is_displayed(),
                                         message=message or _TIMEOUT_MESSAGE.format('enabling', f'{timeout}'))

    def wait_for_presence(self, message=None, timeout=_DEFAULT_TIMEOUT):
        return self._wait(timeout).until(lambda _: self.is_present(),
                                         message=message or _TIMEOUT_MESSAGE.format('presence', f'{timeout}'))

    def wait_for_staleness(self, message=None, timeout=_DEFAULT_TIMEOUT):
        return self._wait(timeout).until(ec.staleness_of(self.web_element),
                                         message=message or _TIMEOUT_MESSAGE.format('staleness', f'{timeout}'))

    def wait_for_text_present(self, text, message=None, timeout=_DEFAULT_TIMEOUT):
        return self._wait(timeout).until(lambda _: self.text == text,
                                         message=message or _TIMEOUT_MESSAGE.format(f'presence of text "{text}"',
                                                                                    f'{timeout}'))

    def wait_for_any_text_present(self, message=None, timeout=_DEFAULT_TIMEOUT):
        return self._wait(timeout).until(lambda _: self.web_element.text != '',
                                         message=message or _TIMEOUT_MESSAGE.format(f'presence of any text ',
                                                                                    f'{timeout}'))

    def find_element(self, by: By, value: str) -> WebElement:
        """Finds element in scope of our web_element"""
        self._wait().until(lambda _: self.web_element.find_element(by, value).is_displayed(),
                           f'Could not wait for child element with locator ({by}, {value})')
        return self.web_element.find_element(by, value)

    def find_elements(self, by: By, value: str) -> List[WebElement]:
        """Finds elements in scope of our web_element"""
        self._wait().until(lambda _: self.web_element.find_element(by, value).is_displayed(),
                           f'Could not wait for child elements with locator ({by}, {value})')
        return self.web_element.find_elements(by, value)

    def find_all(self) -> List[WebElement]:
        """
        Finds all sibling elements
        IMPORTANT: use only when element is initialized by locator
        :return: list of sibling WebElements
        """
        if self._locator is None:
            raise AttributeError(
                'Cannot find siblings without valid locator. Initialize element using locator: Tuple[By, str]')
        self._wait().until(ec.visibility_of_all_elements_located(self._locator),
                           f'Could not wait for sibling elements with locator ({self._locator})')
        return self._finder.find_elements(*self._locator)

    def move_to(self):
        ActionChains(web_driver.driver).move_to_element(self.web_element).perform()

    @property
    def text(self) -> str:
        """Gets text of element"""
        return self.web_element.text

    @property
    def location(self) -> Dict[str, int]:
        """Gets location of element"""
        return self.web_element.location

    @property
    def parent(self) -> WebElement:
        """Gets parent of element"""
        return self.web_element.parent

    @property
    def size(self) -> Dict[str, Any]:
        """Gets size of element"""
        return self.web_element.size

    def get_attribute(self, name: str) -> str:
        """"Gets attribute of element. E.g 'href'"""
        return self.web_element.get_attribute(name)

    @catch_errors()
    def is_enabled(self) -> bool:
        """
        Defines whether element is enabled on a web page
        By default all errors/exceptions are caught. To disable decorator pass argument 'catch=False'.
        E.g is_enabled(catch=False)
        """
        if self._web_element:
            return self._web_element.is_enabled()
        else:
            return self._finder.find_element(*self._locator).is_enabled()

    @catch_errors()
    def is_displayed(self) -> bool:
        """
        Defines whether element is displayed (presence of element within a web page)
        By default all errors/exceptions are caught. To disable decorator pass argument 'catch=False'.
        E.g is_displayed(catch=False)
        """
        if self._web_element:
            return self._web_element.is_displayed()
        else:
            self._finder.find_element(*self._locator).is_displayed()
            return True

    @catch_errors()
    def is_present(self) -> bool:
        """
        Defines whether element is present on page
        By default all errors/exceptions are caught. To disable decorator pass argument 'catch=False'.
        E.g is_present(catch=False)
        """
        if self._web_element:
            return self._web_element.is_displayed()
        else:
            self._finder.find_element(*self._locator)
            return True

    def get_property(self, name: str) -> str:
        """Gets property of element"""
        return self.web_element.get_property(name)

    def value_of_css_property(self, name: str) -> str:
        """Gets value of element`s css property"""
        return self.web_element.value_of_css_property(name)

    def scroll_into_view(self, element: Optional[WebElement] = None) -> None:
        """
        Scrolls to element
        :param element: [Optional] element to scroll to
        """
        target_element = element or self.web_element
        web_driver.driver.execute_script("arguments[0].scrollIntoView();", target_element)
