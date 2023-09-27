from time import time, sleep


class PollingTimeoutExpired(Exception):
    """
    PollingTimeoutException
    """


class Waiter(object):

    @classmethod
    def poll(cls, timeout, func, failure_message=None, time_sleep=1, *args, **kwargs):
        """
        Polls function during given timeout.

        :param int timeout: timeout in seconds.
        :param func: function that will be polled.
        :param str failure_message: failure message, if set then error will
        be raised if condition will not met in given timeout.
        :param args: args that will be passed to function.
        :param kwargs: kwargs that will be passed to function.
        :return: Result of given function if can be interpreted as True,
        otherwise False.
        """
        start_time = time()

        while True:
            result = func(*args, **kwargs)
            if result:
                return result
            elif time() - start_time >= timeout:
                if failure_message is not None:
                    raise PollingTimeoutExpired(failure_message)
                else:
                    return False
            sleep(time_sleep)

    @classmethod
    def poll_request(cls,
                     timeout,
                     request,
                     failure_message=None,
                     predicate=lambda m: True,
                     time_sleep=1,
                     *args, **kwargs):
        """
        Polls request during given timeout.

        :param int timeout: timeout in seconds.
        :param request: request that will be polled.
        :param str failure_message: failure message, if set then error will
        be raised if condition will not met in given timeout.
        :param predicate: function which will applied to response.
        :param args: args that will be passed to request.
        :param kwargs: kwargs that will be passed to request.
        :return: Result of given request
        if can be interpreted as response result,
        otherwise False.
        """
        last_response = []

        def _poll_request():
            last_response[:] = []
            response = request(*args, **kwargs)
            last_response.append(response)
            return predicate(response)

        state = cls.poll(timeout, _poll_request, time_sleep=time_sleep)
        last_response = last_response[-1]
        if state:
            # result = True, last_response
            result = last_response
        else:
            if failure_message is not None:
                raise PollingTimeoutExpired(failure_message)
            else:
                # result = False, last_response
                result = last_response

        return result
