from marshmallow_mongoengine import ModelSchema
from core.base import BaseSchema
from marshmallow import fields
from datetime import datetime


class KeySchema(BaseSchema):
    __envelope_key__ = {'single': 'key'}

    _id = fields.UUID(dump_only=True)
    param_key = fields.Str(required=True)
    created_time = fields.DateTime(default=datetime.utcnow(), dump_only=True)


class KeysSchema(KeySchema):
    __envelope_key__ = {'many': 'key_list'}


class ParamSchema(BaseSchema):
    __envelope_key__ = {'single': 'param'}

    _id = fields.UUID(dump_only=True)

    key_id = fields.UUID(required=True, load_only=True)
    key = fields.Nested(KeySchema, dump_only=True)

    param_value = fields.Str(required=True)
    created_time = fields.DateTime(default=datetime.utcnow(), dump_only=True)
    updated_time = fields.DateTime(default=datetime.utcnow(), dump_only=True)


class ParamsSchema(ParamSchema):
    __envelope_key__ = {'many': 'param_list'}


class UrlSchema(ModelSchema):
    __envelope_key__ = {'single': 'url'}

    _id = fields.UUID(dump_only=True)
    name = fields.Str()

    param_ids = fields.List(fields.UUID(), load_only=True)
    params = fields.List(fields.Nested(ParamSchema), dump_only=True)

    created_time = fields.DateTime(default=datetime.utcnow(), dump_only=True)
    updated_time = fields.DateTime(default=datetime.utcnow(), dump_only=True)


class UrlsSchema(UrlSchema):
    __envelope_key__ = {'many': 'url_list'}


key_schema = KeySchema()
keys_schema = KeySchema(many=True)

param_schema = ParamSchema()
params_schema = ParamsSchema(many=True)

url_schema = UrlSchema()
urls_schema = UrlsSchema(many=True)
