import time
import urllib.parse

from typing import Any
from http import HTTPStatus

from requests.exceptions import ConnectionError
from hamcrest import assert_that, equal_to

from src.clients.http import HttpClient
from src.fixtures import common
from src.schemes.base import ApiResponse
from src.steps.api.models import Meta
from src.utils.common import allure_log, wait_502_disappear


class ForbiddenError(Exception):
    code: HTTPStatus.FORBIDDEN


class BadGatewayError(Exception):
    code: HTTPStatus.BAD_GATEWAY


def assert_that_error(code, eq, text):
    if code == HTTPStatus.FORBIDDEN:
        raise ForbiddenError
    if code == HTTPStatus.BAD_GATEWAY:
        raise BadGatewayError
    assert_that(code, eq, text)


def rerun_failed(func):
    def wrapper(*args, **kwargs):
        try:
            return wait_502_disappear(func, *args, **kwargs)
        except ForbiddenError:
            id, jwt, csrf = common.session_inst.re_login()
            if kwargs.get('cookies'):
                kwargs['cookies'].update(PHPSESSID=id)
            if kwargs.get('form_data'):
                kwargs['form_data'].update(YII_CSRF_TOKEN=csrf)
            return func(*args, **kwargs)
        except BadGatewayError:
            return wait_502_disappear(func, is_check_status=False, *args, **kwargs)
        except ConnectionError:
            time.sleep(180)
            return wait_502_disappear(func, *args, **kwargs)

    return wrapper


class Base(object):
    client: HttpClient = None
    meta: Meta = None

    def __init__(self, client):
        self.client = client

    @rerun_failed
    def get(self, item: Any = None, meta: Meta = None, filters: dict = None, sorting: list = None,
            expected_status_code=HTTPStatus.OK, is_check_status=True, report_allure=True, *args,
            **kwargs) -> ApiResponse:

        meta = meta if meta else self.meta

        path = meta.build_path(item) if item else meta.path

        if filters:
            params = {f'filters[{key}]': value for key, value in filters.items()}
            kwargs.get("params").update(**params) if kwargs.get("params") else kwargs.update(params=params)

        if sorting:
            params = {f'sorting[{num}]': value for num, value in enumerate(sorting)}
            kwargs.get("params").update(**params) if kwargs.get("params") else kwargs.update(params=params)

        query_info = f'GET - {path}' if not kwargs.get(
            'step_info') else f'GET - {path} # step: {kwargs.pop("step_info")}'

        response = self.client.get(url=path, *args, **kwargs)

        allure_log_data = {
            "url": path,
            "response status": response.status_code,
            "response": response.text,
            "query_info": query_info
        }

        if kwargs.get('params'):
            allure_log_data.update(params=kwargs.get('params'))
        if kwargs.get('headers'):
            allure_log_data.update(headers=kwargs.get('headers'))
        if kwargs.get('cookies'):
            allure_log_data.update(cookies=kwargs.get('cookies'))
        if report_allure:
            allure_log(**allure_log_data)
        if is_check_status:
            assert_that_error(response.status_code, equal_to(expected_status_code), response.text)
        if not meta.response_schema:
            raise Exception('Not found schema for list response')
        return ApiResponse(response, meta.response_schema)

    @rerun_failed
    def post(self, item: Any = None, data: dict = None, meta: Meta = None, expected_status_code=HTTPStatus.CREATED,
             form_data=None, is_check_status=True, report_allure=True, *args, **kwargs) -> ApiResponse:

        meta = meta if meta else self.meta

        path = meta.build_path(item) if item else meta.path

        if form_data:
            data = urllib.parse.urlencode(form_data, doseq=True)

        query_info = f'POST - {path}' if not kwargs.get(
            'step_info') else f'POST - {path} # step: {kwargs.pop("step_info")}'

        response = self.client.post(url=path, data=data, *args, **kwargs)

        allure_log_data = {
            "url": path,
            "payload": data,
            "response status": response.status_code,
            "response": response.text,
            "query_info": query_info
        }

        if kwargs.get('json'):
            allure_log_data.update(payload=kwargs.get('json'))
        if kwargs.get('headers'):
            allure_log_data.update(headers=kwargs.get('headers'))
        if kwargs.get('cookies'):
            allure_log_data.update(cookies=kwargs.get('cookies'))
        if report_allure:
            allure_log(**allure_log_data)
        if is_check_status:
            assert_that_error(response.status_code, equal_to(expected_status_code), response.text)
        if not meta.response_schema:
            raise Exception('Not found schema for list response')
        return ApiResponse(response, meta.response_schema)

    @rerun_failed
    def put(self, item: Any = None, meta: Meta = None, expected_status_code=HTTPStatus.NO_CONTENT, is_check_status=True,
            report_allure=True, *args, **kwargs) -> ApiResponse:

        meta = meta if meta else self.meta

        path = meta.build_path(item) if item else meta.path

        query_info = f'PUT - {path}' if not kwargs.get(
            'step_info') else f'PUT - {path} # step: {kwargs.pop("step_info")}'

        response = self.client.put(url=path, *args, **kwargs)

        allure_log_data = {
            "url": path,
            "response status": response.status_code,
            "response": response.text,
            "query_info": query_info
        }

        if kwargs.get('json'):
            allure_log_data.update(payload=kwargs.get('json'))
        if kwargs.get('data'):
            allure_log_data.update(payload=kwargs.get('data'))
        if kwargs.get('headers'):
            allure_log_data.update(headers=kwargs.get('headers'))
        if kwargs.get('cookies'):
            allure_log_data.update(cookies=kwargs.get('cookies'))
        if report_allure:
            allure_log(**allure_log_data)
        if is_check_status:
            assert_that_error(response.status_code, equal_to(expected_status_code), response.text)
        if not meta.response_schema:
            raise Exception('Not found schema for list response')
        return ApiResponse(response, meta.response_schema)

    @rerun_failed
    def patch(self, item: Any = None, meta: Meta = None, is_check_status=True, expected_status_code=HTTPStatus.OK,
              report_allure=True, *args, **kwargs) -> ApiResponse:
        meta = meta if meta else self.meta

        path = meta.build_path(item) if item else meta.path

        query_info = f'PATCH - {path}' if not kwargs.get(
            'step_info') else f'PATCH - {path} # step: {kwargs.pop("step_info")}'

        response = self.client.patch(url=path, *args, **kwargs)

        allure_log_data = {
            "url": path,
            "response status": response.status_code,
            "response": response.text,
            "query_info": query_info
        }

        if kwargs.get('json'):
            allure_log_data.update(payload=kwargs.get('json'))
        if kwargs.get('data'):
            allure_log_data.update(payload=kwargs.get('data'))
        if kwargs.get('headers'):
            allure_log_data.update(headers=kwargs.get('headers'))
        if kwargs.get('cookies'):
            allure_log_data.update(cookies=kwargs.get('cookies'))
        if report_allure:
            allure_log(**allure_log_data)
        if is_check_status:
            assert_that_error(response.status_code, equal_to(expected_status_code), response.text)
        if not meta.response_schema:
            raise Exception('Not found schema for list response')
        return ApiResponse(response, meta.response_schema)

    @rerun_failed
    def delete(self, item: Any = None, meta: Meta = None, expected_status_code=HTTPStatus.NO_CONTENT,
               report_allure=True, *args, **kwargs) -> ApiResponse:
        meta = meta if meta else self.meta

        path = meta.build_path(item) if item else meta.path

        query_info = f'DELETE - {path}' if not kwargs.get(
            'step_info') else f'DELETE - {path} # step: {kwargs.pop("step_info")}'

        response = self.client.delete(url=path, *args, **kwargs)

        allure_log_data = {
            "url": path,
            "response status": response.status_code,
            "response": response.text,
            "query_info": query_info
        }

        if kwargs.get('headers'):
            allure_log_data.update(headers=kwargs.get('headers'))
        if kwargs.get('cookies'):
            allure_log_data.update(cookies=kwargs.get('cookies'))
        if report_allure:
            allure_log(**allure_log_data)
        assert_that_error(response.status_code, equal_to(expected_status_code), response.text)
        if not meta.response_schema:
            raise Exception('Not found schema for list response')
        return ApiResponse(response, meta.response_schema)
