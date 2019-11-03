from .element import Element


class Button(Element):
    """
    Class represents element named as 'Button'
    """

    def click(self):
        """
        Perform 'click' action using implementation WebElement`s 'click' method
        """
        self.wait_for_visibility()
        self.web_element.click()
