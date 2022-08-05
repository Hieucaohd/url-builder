from .services import key_service
from .serializers import key_schema, keys_schema
from api.exceptions import InvalidUsage
from flask_apispec import marshal_with, use_kwargs
from marshmallow import fields
from flask import Blueprint
from utils import LocationParseArgs
from base import delete_response_schema
from utils.docs_register import register_view

blueprint = Blueprint('key', __name__)


@blueprint.route('/api/keys', methods=('GET',))
@use_kwargs({'page': fields.Int(), 'per_page': fields.Int(), 'sort': fields.Str()}, location=LocationParseArgs.querystring.value)
@marshal_with(keys_schema)
def get_keys(page=0, per_page=10, sort=""):
    key_instances = key_service.get_many_instances(page=page, per_page=per_page, sort=sort)
    return key_instances


@blueprint.route('/api/keys/<key_id>', methods=('GET',))
@marshal_with(key_schema)
def get_key(key_id=None):
    key_instance = key_service.get_instance_by_id(key_id)
    if not key_instance:
        raise InvalidUsage.param_key_not_found()
    return key_instance


@blueprint.route('/api/keys', methods=('POST',))
@use_kwargs(key_schema, location=LocationParseArgs.json.value)
@marshal_with(key_schema)
def make_key(**kwargs):
    key_instance = key_service.create_instance({"param_key": kwargs['param_key']})
    return key_instance


@blueprint.route('/api/keys/many', methods=('POST',))
@use_kwargs(keys_schema, location=LocationParseArgs.json.value)
@marshal_with(keys_schema)
def make_keys(*key_list):
    key_instances = key_service.bulk_create_instances(key_list)
    return key_instances


@blueprint.route('/api/keys/<key_id>', methods=('PUT',))
@use_kwargs(key_schema, location=LocationParseArgs.json.value)
@marshal_with(key_schema)
def update_key(key_id, **kwargs):
    key_updated = key_service.update_instance_by_id(key_id, kwargs)
    if not key_updated:
        raise InvalidUsage.param_key_not_found()
    return key_updated


@blueprint.route('/api/keys/<key_id>', methods=('DELETE',))
@marshal_with(delete_response_schema)
def delete_key(key_id):
    delete_count = key_service.delete_instance_by_id(key_id)
    return {
        "success": delete_count
    }


def register_docs(docs):
    register_view(docs, blueprint, [
        get_keys,
        get_key,
        make_key,
        make_keys,
        update_key,
        delete_key
    ])

