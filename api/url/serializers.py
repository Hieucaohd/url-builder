from base import BaseSchema
from marshmallow import fields, post_load
from utils.objectID_convert import convert_to_object_id
from api.param.serializers import QuickCreateParamSchema


def convert_list_ids(list_id):
    result = []
    for id in list_id:
        result.append(convert_to_object_id(id))
    return result


class UrlSchema(BaseSchema):
    __envelope_key__ = {'single': 'url'}

    _id = fields.UUID(dump_only=True)
    name = fields.Str()
    param_ids = fields.List(fields.Str())
    created_time = fields.DateTime(dump_only=True)
    updated_time = fields.DateTime(dump_only=True)

    @post_load(pass_many=True)
    def convert_param_ids(self, data, many, **kwargs):
        if many:
            for data_info in data:
                if 'param_ids' in data_info:
                    data_info['param_ids'] = convert_list_ids(data_info['param_ids'])
        else:
            if 'param_ids' in data:
                data['param_ids'] = convert_list_ids(data['param_ids'])
        return data


class UrlsSchema(UrlSchema):
    __envelope_key__ = {'many': 'url_list'}


url_schema = UrlSchema()
urls_schema = UrlsSchema(many=True)


class CreateUrlSchema(UrlSchema):
    param_ids = fields.List(fields.Str(), required=True)


class CreateManyUrlSchema(CreateUrlSchema):
    __envelope_key__ = {'many': 'url_list'}


create_url_schema = CreateUrlSchema()
create_many_url_schema = CreateManyUrlSchema(many=True)


class QuickCreateUrlSchema(BaseSchema):
    __envelope_key__ = {'single': 'url'}

    name = fields.Str()
    param_list = fields.List(fields.Nested(QuickCreateParamSchema))


quick_create_url_schema = QuickCreateUrlSchema()
