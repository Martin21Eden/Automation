from .element import Element


class TextElement(Element):
    """
    Class represents element with text
    """

    @property
    def text(self):
        self.wait_for_any_text_present()
        return self.web_element.text
