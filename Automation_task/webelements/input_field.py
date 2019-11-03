from .element import Element


class InputField(Element):
    """
    Class represents element of input field type
    """

    def set_text(self, text):
        """
        Clears text field and sets given text
        :param text: string to be set to text field
        """
        self.clear().send_keys(text)

    def clear(self):
        """
        Clears text field using WebElement`s clear 'method'
        """
        self.wait_for_visibility()
        self.web_element.clear()
        return self

    def send_keys(self, text):
        """
        Sets given text to text field
        :param text: string to be set to text field
        """
        self.wait_for_visibility()
        self.web_element.send_keys(text)
        return self
