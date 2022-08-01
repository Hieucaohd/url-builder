from mongo import MongoDBInit
from mongo.index.parse_indexes import create_mongo_indexes
from .base_meta_model import BaseMetaModel

from .query_set import QuerySet


class BaseMongoDB(object, metaclass=BaseMetaModel):

    @classmethod
    def setup_collection(cls):
        cls.collection = MongoDBInit.get_db()[cls.COLLECTION_NAME]
        cls.objects = QuerySet(cls.collection)
        cls.create_indexes()

    @classmethod
    def create_indexes(cls, indexes=None):

        if indexes is None and hasattr(cls, "meta"):
            indexes = cls.meta.get('indexes', None)

        if indexes is None:
            return

        create_mongo_indexes(cls.collection, indexes)



