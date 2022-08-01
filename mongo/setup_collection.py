from mongo import MongoDBInit
from .query_set import QuerySet


models = []


def register_collection(class_model):
    global models
    models.append(class_model)


def setup_collection_model():
    db = MongoDBInit.get_db()
    for model in models:
        collection = db[model.COLLECTION_NAME]
        model.collection = collection
        model.objects = QuerySet(collection)
        model.create_indexes()

