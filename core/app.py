from flask import Flask

from core.extensions import cache, cors

from core.settings import ProdConfig
from core.exceptions import InvalidUsage

from flask_mongoengine import MongoEngine

from core import param_handler


def create_app(config_object=ProdConfig):
    """An application factory."""

    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)

    db = MongoEngine()
    db.init_app(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""

    cache.init_app(app)
    cors.init_app(app)


def register_blueprints(app: Flask):
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(param_handler.views.blueprint, origins=origins)

    app.register_blueprint(param_handler.views.blueprint)


def register_error_handlers(app: Flask):

    def error_handler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(error_handler)

