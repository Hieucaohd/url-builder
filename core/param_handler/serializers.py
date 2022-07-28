from marshmallow_mongoengine import ModelSchema
from .models import Key, Param, Url


class KeySchema(ModelSchema):
    class Meta:
        model = Key


class ParamSchema(ModelSchema):
    class Meta:
        model = Param


class UrlSchema(ModelSchema):
    class Meta:
        model = Url


key_schema = KeySchema()
param_schema = ParamSchema()
url_schema = UrlSchema()
