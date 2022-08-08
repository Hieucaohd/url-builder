from pymongo import MongoClient
import copy


global_mongodb_client = None
mongo_config = None


class MongoDBInit(object):
    app = None

    @staticmethod
    def init_client(mongo_uri=None, config=None):
        global global_mongodb_client
        global mongo_config

        if mongo_config is None and config is not None:
            mongo_config = copy.deepcopy(config)

        if mongo_uri is None:
            mongo_uri = mongo_config['MONGO_URI']

        if global_mongodb_client is None:
            global_mongodb_client = MongoClient(mongo_uri, connect=False)

        from mongo.setup_collection import setup_collection_model
        setup_collection_model()

    @staticmethod
    def init_app(app):
        global global_mongodb_client
        global mongo_config

        if mongo_config is None:
            mongo_config = copy.deepcopy(app.config["MONGO_DB_SETTINGS"])

        if global_mongodb_client is None:
            global_mongodb_client = MongoClient(mongo_config["MONGO_URI"])

        from mongo.setup_collection import setup_collection_model
        setup_collection_model()

    @staticmethod
    def get_db(db_name=None, mongo_uri=None):
        assert global_mongodb_client is not None, "You must call MongoDBInit.init_app(app) or " \
                                                  "MongoDBInit.init_client first"
        if db_name is None:
            assert mongo_config is not None, "no config provided."
            db_name = mongo_config["DB_NAME"]

        if mongo_uri is None:
            return global_mongodb_client[db_name]

        return MongoClient(mongo_uri, connect=False)[db_name]

    @staticmethod
    def get_mongo_db_client():
        assert global_mongodb_client is not None, "You must call MongoDBInit.init_app(app) or " \
                                                  "MongoDBInit.init_client first"
        return global_mongodb_client
