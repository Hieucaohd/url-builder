from base import BaseSchema
from marshmallow import fields


class KeySchema(BaseSchema):
    __envelope_key__ = {'single': 'key'}

    _id = fields.UUID(dump_only=True)
    param_key = fields.Str(required=True)
    created_time = fields.DateTime(dump_only=True)
    updated_time = fields.DateTime(dump_only=True)


class KeysSchema(KeySchema):
    __envelope_key__ = {'many': 'key_list'}


key_schema = KeySchema()
keys_schema = KeysSchema(many=True)
