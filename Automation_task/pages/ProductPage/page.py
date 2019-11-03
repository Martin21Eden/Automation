from .locators import ProductLocators as _product_locators
from .locators import HeaderLocators as _header_locators
from Automation_task.webelements import InputField, Button, TextElement
from Automation_task.pages.BasePage import BasePage


class Header:
    """
    The class describes header of site
    """
    SEARCH_FIELD = InputField(_header_locators.SEARCH_INPUT)
    SEARCH_BUTTON = Button(_header_locators.SEARCH_BUTTON)

    def search_product(self, text: str):
        self.SEARCH_FIELD.set_text(text)
        self.SEARCH_BUTTON.click()


class ProductPage(BasePage, Header):
    """
    The class describes page of product
    """
    PRODUCT_TITTLE = TextElement(_product_locators.TITTLE_PRODUCT)

    def is_opened(self):
        return self.PRODUCT_TITTLE.is_displayed()
