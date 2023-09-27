import json

from hamcrest import assert_that, has_entries
from marshmallow import fields, Schema
from requests import Response


class BaseObject:
    schema = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    @property
    def json(self):
        return self.schema().dump(self)

    def is_contains(self, **kwargs):
        return assert_that(self.json, has_entries(**kwargs))


class ApiResponse:
    def __init__(self, response: Response, schema: Schema):
        self.original_response = response
        self.schema = schema

    @property
    def status_code(self):
        return self.original_response.status_code

    @property
    def text(self):
        return self.original_response.text

    @property
    def headers(self):
        return self.original_response.headers

    @property
    def json(self):
        return self.original_response.json()

    @property
    def cookies(self):
        return self.original_response.cookies

    @property
    def url(self):
        return self.original_response.url

    @property
    def obj(self):
        return self.schema().loads(self.original_response.content)

    @property
    def obj_list(self):
        return self.schema(many=True).loads(self.original_response.content)

    @property
    def obj_items(self):
        return self.schema().loads(json.dumps({'items': json.loads(self.original_response.content)}))

    def inner_items(self, item):
        return self.schema(many=True).loads(json.dumps(json.loads(self.original_response.content)[item]))

    def inner_items_to_list(self, item, many=True):
        return self.schema(many=many).loads(
            json.dumps([values for key, values in json.loads(self.original_response.content)[item].items()]))

    def inner_item(self, item):
        return self.schema().loads(json.dumps(json.loads(self.original_response.content)[item]))


class SkipListNested(fields.Nested):

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, dict):
            return value
        else:
            return None


class SkipList(fields.String):

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, list):
            return None
        return value


class SkipString(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, list):
            return value
        elif isinstance(value, int):
            return value
        else:
            return None


class ConvertInteger2String(fields.String):

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, str):
            return value
        else:
            return None
