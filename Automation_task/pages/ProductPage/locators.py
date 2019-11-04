from selenium.webdriver.common.by import By


class HeaderLocators:
    SEARCH_INPUT = (By.CSS_SELECTOR, 'div.header-search.js-app-search-suggest input')
    SEARCH_BUTTON = (By.CSS_SELECTOR, 'div.header-search.js-app-search-suggest > form > button')


class ProductLocators:
    TITLE_PRODUCT = (By.CSS_SELECTOR, 'body h1')
