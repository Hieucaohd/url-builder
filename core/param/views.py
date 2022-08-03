from flask import Blueprint
from .services import param_service
from .serializers import (
    param_schema,
    params_schema,
    create_param_schema,
    create_many_param_schema,
    quick_create_param_schema,
    quick_create_many_param_schema,
    param_result_with_key_schema,
    params_result_with_key_schema
)
from flask_apispec import use_kwargs, marshal_with
from utils import LocationParseArgs
from marshmallow import fields
from core.base.serializer import delete_response_schema
from core.exceptions import InvalidUsage
from utils.docs_register import register_view

blueprint = Blueprint('param', __name__)


@blueprint.route('/api/params', methods=('POST',))
@use_kwargs(create_param_schema, location=LocationParseArgs.json.value)
@marshal_with(create_param_schema)
def make_param(**kwargs):
    param_instance = param_service.create_instance(kwargs)
    return param_instance


@blueprint.route('/api/params/quick', methods=('POST',))
@use_kwargs(quick_create_param_schema, location=LocationParseArgs.json.value)
@marshal_with(param_schema)
def make_quick_param(**kwargs):
    param_instance = param_service.quick_create_param(kwargs)
    return param_instance


@blueprint.route('/api/params/quick/many', methods=('POST',))
@use_kwargs(quick_create_many_param_schema, location=LocationParseArgs.json.value)
@marshal_with(params_schema)
def make_quick_params(*param_list):
    param_instances = param_service.quick_bulk_create_params(param_list)
    return list(param_instances)


@blueprint.route('/api/params/many', methods=('POST',))
@use_kwargs(create_many_param_schema, location=LocationParseArgs.json.value)
@marshal_with(create_many_param_schema)
def make_params(*param_list):
    param_instances = param_service.bulk_create_instances(param_list)
    return param_instances


@blueprint.route('/api/params/<param_id>', methods=('GET',))
@marshal_with(param_schema)
def get_param(param_id):
    param_instance = param_service.get_instance_by_id(param_id)
    if not param_instance:
        raise InvalidUsage.param_not_found_error()
    return param_instance


@blueprint.route('/api/params/<param_id>/with_key', methods=('GET',))
@marshal_with(param_result_with_key_schema)
def get_param_with_key(param_id):
    param_instance = param_service.get_param_with_key(param_id)
    if not param_instance:
        raise InvalidUsage.param_not_found_error()
    return param_instance


@blueprint.route('/api/params', methods=('GET',))
@use_kwargs({'page': fields.Int(), 'per_page': fields.Int(), 'sort': fields.Str()}, location=LocationParseArgs.querystring.value)
@marshal_with(params_schema)
def get_params(page=0, per_page=10, sort=""):
    param_instances = param_service.get_many_instances(page=page, per_page=per_page, sort=sort)
    return param_instances


@blueprint.route('/api/params/with_key', methods=('GET',))
@use_kwargs({'page': fields.Int(), 'per_page': fields.Int(), 'sort': fields.Str()}, location=LocationParseArgs.querystring.value)
@marshal_with(params_result_with_key_schema)
def get_params_with_key(page=0, per_page=10, sort=""):
    param_instances = param_service.get_many_param_with_key(page=page, per_page=per_page, sort=sort)
    return param_instances


@blueprint.route('/api/params/<param_id>', methods=('PUT',))
@use_kwargs(param_schema, location=LocationParseArgs.json.value)
@marshal_with(param_schema)
def update_param(param_id, **kwargs):
    updated_param = param_service.update_instance_by_id(param_id, kwargs)
    if not updated_param:
        raise InvalidUsage.param_not_found_error()
    return updated_param


@blueprint.route('/api/params/<param_id>', methods=('DELETE',))
@marshal_with(delete_response_schema)
def delete_param(param_id):
    delete_count = param_service.delete_instance_by_id(param_id)
    return {
        "success": delete_count
    }


def register_docs(docs):
    register_view(docs, blueprint, [
        delete_param,
        update_param,
        get_params,
        get_param,
        get_param_with_key,
        get_params_with_key,
        make_param,
        make_quick_param,
        make_params,
        make_quick_params,
    ])

