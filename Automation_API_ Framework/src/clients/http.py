import requests


class HttpClient:
    def __init__(self, host):
        self.host = host

    def request(self, method: str, *args, **kwargs):
        if kwargs.get("token"):
            headers = {"Authorization": f'Bearer {kwargs.pop("token")}'}
            if not kwargs.get('headers'):
                kwargs.update({"headers": headers})
            else:
                kwargs['headers'].update(**headers)
        return getattr(requests, method)(*args, **kwargs)

    def get(self, url: str, *args, **kwargs):
        return self.request('get', url=self.host + url, *args, **kwargs)

    def post(self, url: str, *args, **kwargs):
        return self.request('post', url=self.host + url, *args, **kwargs)

    def put(self, url: str, *args, **kwargs):
        return self.request('put', url=self.host + url, *args, **kwargs)

    def patch(self, url: str, *args, **kwargs):
        return self.request('patch', url=self.host + url, *args, **kwargs)

    def delete(self, url: str, *args, **kwargs):
        return self.request('delete', url=self.host + url, *args, **kwargs)
