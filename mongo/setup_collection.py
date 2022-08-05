from mongo import MongoDBInit
from .query_set import QuerySet


models = []


def register_collection(class_model):
    global models
    models.append(class_model)


def setup_collection_model():
    db_default = MongoDBInit.get_db()
    for model in models:
        db = None
        if hasattr(model, 'DB_NAME'):
            db = MongoDBInit.get_mongo_db_client()[model.DB_NAME]

        if db is None:
            db = db_default

        collection = db[model.COLLECTION_NAME]
        model.collection = collection
        model.objects = QuerySet(collection)
        model.create_indexes()

