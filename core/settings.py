"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('URL_BUILDER_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))   # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    CACHE_TYPE = "simple"   # Can be "memcached", "redis", etc.
    CORS_ORIGIN_WHITELIST = []


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    MONGODB_SETTINGS = [
        {
            'db': os.environ.get('DB_NAME', 'prodDB'),
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': os.environ.get('DB_PORT', 27017),
            'alias': 'default'
        }
    ]


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'devDB'
    DB_PATH = None
    MONGODB_SETTINGS = [
        {
            'db': 'devDB',
            'host': 'localhost',
            'port': 27017,
            'alias': 'default'
        }
    ]
    CACHE_TYPE = 'simple'   # Can be "memcached", "redis", etc


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    MONGODB_SETTINGS = [
        {
            'db': 'testDB',
            'host': 'localhost',
            'port': 27017,
            'alias': 'default'
        }
    ]
