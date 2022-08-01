"""Application configuration."""
import os
"""
mongodb+srv://hieucao192:helloworld123@authenticationtest.6lh8w.mongodb.net/?retryWrites=true&w=majority
"""


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
    MONGO_DB_SETTINGS = {
        "MONGO_URI": os.environ.get("MONGO_URL", "mongodb://localhost:27017"),
        "DB_NAME": os.environ.get("DB_NAME", "prodDB")
    }


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'devDB'
    DB_PATH = None
    MONGO_DB_SETTINGS = {
        "MONGO_URI": os.environ.get("MONGO_URL", "mongodb://localhost:27017"),
        "DB_NAME": os.environ.get("DB_NAME", "devDB")
    }
    CACHE_TYPE = 'simple'   # Can be "memcached", "redis", etc


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    MONGO_DB_SETTINGS = {
        "MONGO_URI": os.environ.get("MONGO_URL", "mongodb://localhost:27017"),
        "DB_NAME": os.environ.get("DB_NAME", "testDB")
    }
