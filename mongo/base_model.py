from mongo import MongoDBInit
from mongo.index_collection.parse_indexes import create_mongo_indexes
from .base_meta_model import BaseMetaModel

from .query_set import QuerySet
from pymongo.collection import Collection


class BaseMongoDB(object, metaclass=BaseMetaModel):
    collection: Collection = None

    @classmethod
    def create_indexes(cls, indexes=None):

        if indexes is None and hasattr(cls, "meta"):
            indexes = cls.meta.get('indexes', None)

        if indexes is None:
            print(f"No indexes provided for {cls.COLLECTION_NAME}, skip create index.")
            return

        create_mongo_indexes(cls.collection, indexes)
        print(f"Collection {cls.COLLECTION_NAME}: successfully create index: {indexes}")



