from .page import ProductPage


class ProductPageFlow:
    """
    The class describes the behavior of ProductPage
    """
    _page = ProductPage()

    def search_product(self, text: str):
        self._page.search_product(text)

    @property
    def product_tittle(self):
        self._page.wait_for_page_to_open()
        return self._page.PRODUCT_TITTLE.text
