from .services import key_service
from .serializers import key_schema
from core.exceptions import InvalidUsage
from flask_apispec import marshal_with, use_kwargs
from marshmallow import fields
from flask import Blueprint


blueprint = Blueprint('key', __name__)


@blueprint.route('/api/keys/<key_id>', methods=('GET',))
@marshal_with(key_schema)
def get_key(key_id=None):
    key_instance = key_service.get_instance_by_id(key_id)
    if not key_instance:
        raise InvalidUsage.key_not_found()
    return key_instance


@blueprint.route('/api/keys', methods=('GET',))
@marshal_with(key_schema)
def get_key(key_id=None):
    key_instance = key_service.get_instance_by_id(key_id)
    if not key_instance:
        raise InvalidUsage.key_not_found()
    return key_instance


@blueprint.route('/api/keys', methods=('POST',))
@use_kwargs({'param_key': fields.Str()})
@marshal_with(key_schema)
def make_key(param_key=None):
    key_instance = key_service.create_instance(param_key=param_key)
    return key_instance
