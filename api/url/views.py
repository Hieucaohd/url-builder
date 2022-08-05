from flask import Blueprint
from .serializers import create_url_schema, url_schema, urls_schema, quick_create_url_schema
from flask_apispec import use_kwargs, marshal_with
from .services import url_service
from utils import LocationParseArgs
from api.exceptions import InvalidUsage
from marshmallow import fields
from base import delete_response_schema
from flask_apispec import FlaskApiSpec
from utils.docs_register import register_view

blueprint = Blueprint('url', __name__)


@blueprint.route('/api/urls', methods=('POST',))
@use_kwargs(create_url_schema, location=LocationParseArgs.json.value)
@marshal_with(create_url_schema)
def create_url(**kwargs):
    url_instance = url_service.create_instance(kwargs)
    return url_instance


@blueprint.route('/api/urls/quick', methods=('POST',))
@use_kwargs(quick_create_url_schema, location=LocationParseArgs.json.value)
@marshal_with(url_schema)
def quick_create_url(**kwargs):
    url_instance = url_service.quick_create_url(kwargs)
    return url_instance


@blueprint.route('/api/urls/<url_id>', methods=('GET',))
@marshal_with(url_schema)
def get_url(url_id):
    url_instance = url_service.get_instance_by_id(url_id)
    if not url_instance:
        raise InvalidUsage.url_not_found_error()
    return url_instance


@blueprint.route('/api/urls', methods=('GET',))
@use_kwargs({'page': fields.Int(),
             'per_page': fields.Int(),
             'sort': fields.Str()},
            location=LocationParseArgs.querystring.value)
@marshal_with(urls_schema)
def get_urls(page=0, per_page=10, sort=""):
    url_instances = url_service.get_many_instances(page=page, per_page=per_page, sort=sort)
    return url_instances


@blueprint.route('/api/urls/<url_id>/string', methods=('GET',))
def get_url_string(url_id):
    print(f'{url_id=}')
    url_string = url_service.get_url_string(url_id)
    return {
        "url_string": url_string
    }


@blueprint.route('/api/urls/<url_id>', methods=('PUT',))
@use_kwargs(url_schema, location=LocationParseArgs.json.value)
@marshal_with(url_schema)
def update_url(url_id, **kwargs):
    updated_url = url_service.update_instance_by_id(url_id, kwargs)
    if not updated_url:
        raise InvalidUsage.url_not_found_error()
    return updated_url


@blueprint.route('/api/urls/<url_id>', methods=('DELETE',))
@marshal_with(delete_response_schema)
def delete_url(url_id):
    delete_count = url_service.delete_instance_by_id(url_id)
    return {
        "success": delete_count
    }


def register_docs(docs: FlaskApiSpec):
    register_view(docs, blueprint, [
        create_url,
        quick_create_url,
        get_url,
        get_url_string,
        update_url,
        delete_url
    ])
