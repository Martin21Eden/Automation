from marshmallow import Schema, fields, post_load

from src.schemes.base import BaseObject


class AssetTypeSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    isActive = fields.Boolean(required=True)
    isTargetLanguage = fields.Boolean(required=True)
    isSourceLanguage = fields.Boolean(required=True)
    createdAt = fields.DateTime(required=True)
    updatedAt = fields.DateTime(required=True)


    @post_load
    def make_response_success(self, data, **kwargs):
        return AssetTypeResponse(**data)


class AssetTypeResponse(BaseObject):
    schema = AssetTypeSchema

    @property
    def ok(self):
        return hasattr(self, "createdAt")

