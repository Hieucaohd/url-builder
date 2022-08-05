from flask import Flask

from api.extensions import cache, cors

from api.settings import ProdConfig
from api.exceptions import InvalidUsage

from mongo.base_model import MongoDBInit

import api.param_key
import api.param
import api.url
import api.history_access
from flask_apispec import FlaskApiSpec


def create_app(config_object=ProdConfig):
    """An application factory."""

    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)

    register_extensions(app)
    register_error_handlers(app)
    register_blueprints(app)

    MongoDBInit.init_app(app)

    docs = FlaskApiSpec(app)
    register_blueprint_for_docs(docs)
    return app


def register_extensions(app):
    """Register Flask extensions."""

    cache.init_app(app)
    cors.init_app(app)


def register_blueprint_for_docs(docs: FlaskApiSpec):
    api.url.views.register_docs(docs)
    api.param_key.views.register_docs(docs)
    api.history_access.views.register_docs(docs)
    api.param.views.register_docs(docs)


def register_blueprints(app: Flask):
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')

    cors.init_app(api.param_key.views.blueprint, origins=origins)
    cors.init_app(api.url.views.blueprint, origins=origins)
    cors.init_app(api.param.views.blueprint, origins=origins)
    cors.init_app(api.history_access.views.blueprint, origins=origins)

    app.register_blueprint(api.param_key.views.blueprint)
    app.register_blueprint(api.url.views.blueprint)
    app.register_blueprint(api.param.views.blueprint)
    app.register_blueprint(api.history_access.views.blueprint)


def register_error_handlers(app: Flask):

    def error_handler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(error_handler)
