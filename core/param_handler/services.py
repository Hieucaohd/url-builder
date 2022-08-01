import pymongo
import pymongo.errors
from bson import ObjectId

from .models import Key
from core.base import BaseService
import mongoengine
from core.exceptions import InvalidUsage
from .serializers import keys_schema, key_schema
from mongoengine import get_connection, get_db


class KeyService(BaseService):
    model = Key

    def create_instance(self, **kwargs):
        try:
            instance = super().create_instance(**kwargs)
            return instance
        except (mongoengine.errors.BulkWriteError, mongoengine.errors.NotUniqueError) as e:
            raise InvalidUsage.param_key_duplicate_error()

    def bulk_create_instances(self, data_list: list, ignore_invalid_data=True):
        try:
            instances = super().bulk_create_instances(data_list, ignore_invalid_data)
            return instances
        except (mongoengine.errors.BulkWriteError, mongoengine.errors.NotUniqueError) as e:
            keys_exist = self.find_key_exist([key.param_key for key in data_list])
            keys_exist = keys_schema.dump(keys_exist)
            raise InvalidUsage.param_key_duplicate_error(keys_exist)

    def bulk_create_instances_pymongo(self, data_list: list, ignore_invalid_data=True):
        error = False
        result_ids: [ObjectId] = []
        native_conn = get_connection()
        with native_conn.start_session() as session:
            with session.start_transaction() as db:
                try:
                    db = native_conn.get_database('devDB')
                    collection = db.get_collection('key')
                    result = collection.insert_many([data.to_mongo() for data in data_list], session=session)
                    result_ids = result.inserted_ids
                except pymongo.errors.BulkWriteError as e:
                    session.abort_transaction()
                    error = True

        if error:
            keys_exist = self.find_key_exist([key.param_key for key in data_list])
            list_key_error = keys_schema.dump(keys_exist)
            raise InvalidUsage.param_key_duplicate_error(list_key_error)

        print(result_ids)
        ids = [str(result_id) for result_id in result_ids]
        print(ids)
        return []

    def find_key_exist(self, key_list):
        keys_exist = self.get_many_instances(param_key__in=key_list)
        return keys_exist


key_service = KeyService()
