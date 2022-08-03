import pymongo
import pymongo.errors

from .models import Key
from core.base import BaseService, KeyUniqueBaseService
from core.exceptions import InvalidUsage
from .serializers import keys_schema


class KeyService(KeyUniqueBaseService):
    model = Key

    def create_duplicate_error(self, data_error=None):
        raise InvalidUsage.param_key_duplicate_error()

    def bulk_create_duplicate_error(self, data_error=None):
        keys_exist = self.find_key_exist([key['param_key'] for key in data_error])
        keys_exist = keys_schema.dump(keys_exist)
        raise InvalidUsage.param_key_duplicate_error(keys_exist)

    def find_key_exist(self, key_list):
        keys_exist = self.get_many_instances({"param_key": {"$in": key_list}})
        return keys_exist

    def update_duplicate_error(self, data_error=None):
        raise InvalidUsage.param_key_duplicate_error()


key_service = KeyService()
