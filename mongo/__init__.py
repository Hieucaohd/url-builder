from pymongo import MongoClient


global_mongodb_client = None
mongo_config = None


class MongoDBInit(object):
    app = None

    @staticmethod
    def init_app(app):
        global global_mongodb_client
        global mongo_config

        MongoDBInit.app = app

        if mongo_config is None:
            mongo_config = app.config["MONGO_DB_SETTINGS"]

        if global_mongodb_client is None:
            global_mongodb_client = MongoClient(mongo_config["MONGO_URI"], connect=False)

        from mongo.setup_collection import setup_collection_model
        setup_collection_model()

    @staticmethod
    def get_db(db_name=None):
        if db_name is None:
            db_name = MongoDBInit.app.config["DB_NAME"]

        return global_mongodb_client[db_name]

    @staticmethod
    def get_mongo_db_client():
        assert global_mongodb_client is not None, "You must call MongoDBInit.init_app(app) first"
        return global_mongodb_client
