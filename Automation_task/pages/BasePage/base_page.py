import time
from typing import Callable, Tuple, Any, Union


class BasePage:
    """
    The base class for all pages
    """
    _timeout = 30

    def is_opened(self) -> bool:
        """
        Defines whether WebPage is opened
        :return True if WebPage is opened else False
        """
        raise NotImplementedError(f"'is_opened' method is not implemented in '{self.__class__.__name__}' class")

    def wait_for_page_to_open(self, timeout: int = None):
        """
        Waits for WebPage to be opened and loaded
        """
        fail_msg = f'Could not wait for "{self.__class__.__name__}" ' \
                   f'to open anymore. Tried for {self._timeout} seconds'
        wait_for(self.is_opened, message=fail_msg, timeout=timeout or self._timeout)


def wait_for(callable_condition: Callable, timeout: int = 30, poll: float = 0.5, message: str = '',
             ignored_exceptions: Tuple = (), raise_error: bool = False) -> Union[bool, Any]:
    """
    The function supply wait element
    """
    fail_time = time.time() + timeout
    while time.time() < fail_time:
        try:
            result = callable_condition()
            if result:
                return result
        except Exception as e:
            if e.__class__ not in ignored_exceptions:
                raise e
        time.sleep(poll)
    else:
        if raise_error:
            raise TimeoutError(message)
        else:
            return False
