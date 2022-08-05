from base import BaseSchema
from marshmallow import fields, post_load
from utils.objectID_convert import convert_to_object_id


class ParamSchema(BaseSchema):
    __envelope_key__ = {'single': 'param'}

    _id = fields.UUID(dump_only=True)
    key_id = fields.Str()
    param_value = fields.Str()
    created_time = fields.DateTime(dump_only=True)
    updated_time = fields.DateTime(dump_only=True)

    @post_load(pass_many=True)
    def convert_key_id(self, data, many, **kwargs):
        if many:
            for data_info in data:
                if 'key_id' in data_info:
                    data_info['key_id'] = convert_to_object_id(data_info['key_id'])
        else:
            if 'key_id' in data:
                data['key_id'] = convert_to_object_id(data['key_id'])
        return data


class ParamsSchema(ParamSchema):
    __envelope_key__ = {'many': 'param_list'}


class CreateParamSchema(ParamSchema):
    key_id = fields.Str(required=True)
    param_value = fields.Str(required=True)


class CreateManyParamSchema(CreateParamSchema):
    __envelope_key__ = {'many': 'param_list'}


param_schema = ParamSchema()
params_schema = ParamsSchema(many=True)

create_param_schema = CreateParamSchema()
create_many_param_schema = CreateManyParamSchema(many=True)


class ParamResultWithKeySchema(ParamSchema):
    __envelope_key__ = {'single': "param", "many": "param_list"}
    param_key = fields.Str()


param_result_with_key_schema = ParamResultWithKeySchema()
params_result_with_key_schema = ParamResultWithKeySchema(many=True)


class QuickCreateParamSchema(BaseSchema):
    __envelope_key__ = {'single': 'param'}

    param_key = fields.Str(required=True)
    param_value = fields.Str(required=True)


class QuickCreateManyParamSchema(QuickCreateParamSchema):
    __envelope_key__ = {'many': 'param_list'}


quick_create_param_schema = QuickCreateParamSchema()
quick_create_many_param_schema = QuickCreateManyParamSchema(many=True)

