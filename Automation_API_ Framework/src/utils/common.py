import re
import random
import allure

from src.utils.waiter import Waiter


def generate_random_value(min_v=0, max_v=999999):
    return random.randint(min_v, max_v)


search = lambda pattern, text: re.search(pattern, text).group(1)
findall = lambda pattern, text: re.findall(pattern, text)


def wait_502_disappear(requests, *args, **kwargs):
    return Waiter.poll_request(300,
                               requests,
                               'Got 502 error after 300 sec',
                               lambda res: res.status_code != 502,
                               5,
                               *args,
                               **kwargs)


@allure.step('{query_info}')
def allure_log(**kwargs):
    pass
