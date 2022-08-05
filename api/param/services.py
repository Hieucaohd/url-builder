from base import KeyUniqueBaseService
from api.exceptions import InvalidUsage
from .models import Param
from .serializers import params_schema
from api.param_key.services import key_service
from pymongo import ReturnDocument
from utils.objectID_convert import convert_to_object_id


class ParamService(KeyUniqueBaseService):
    model = Param

    def get_param_with_key(self, param_id):
        param_id = convert_to_object_id(param_id)
        key_collection_name = key_service.model.COLLECTION_NAME
        pipeline = [
            {
                "$lookup": {
                    "from": key_collection_name,
                    "localField": 'key_id',
                    "foreignField": '_id',
                    "as": "keys"
                }
            },
            {
                "$match": {
                    "_id": param_id
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "param_key": {"$first": "$keys.param_key"},
                    "param_value": 1,
                    "created_time": 1,
                    "updated_time": 1,
                    "key_id": 1
                }
            }
        ]
        params = self.model.collection.aggregate(pipeline)
        params = list(params)
        if len(params) == 0:
            return None
        params = params[0]
        return params

    def get_many_param_with_key(self, page, per_page, sort):
        key_collection_name = key_service.model.COLLECTION_NAME
        pipeline = [
            {
                "$lookup": {
                    "from": key_collection_name,
                    "localField": 'key_id',
                    "foreignField": '_id',
                    "as": "keys"
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "param_key": {"$first": "$keys.param_key"},
                    "param_value": 1,
                    "created_time": 1,
                    "updated_time": 1,
                    "key_id": 1
                }
            }
            ,
            {
                "$limit": per_page
            },
            {
                "$skip": page
            }
        ]

        if sort != "" and sort is not None:
            pipeline.append({
                "$sort": {
                    sort: 1
                }
            })
        params = list(self.model.collection.aggregate(pipeline))
        return params

    def quick_create_param(self, data):
        key = key_service.find_one_and_update(
            {"param_key": data['param_key']},
            {"param_key": data['param_key']},
            return_document=ReturnDocument.AFTER,
            upsert=True
        )
        data['key_id'] = key['_id']
        del data['param_key']

        new_param = self.create_instance(data)
        return new_param

    def quick_bulk_create_params(self, list_data: '[{"param_key": "value", "param_value": "value"}]'):
        keys = []
        param_keys = [data['param_key'] for data in list_data]
        keys_existed = key_service.get_many_instances({"param_key": {"$in": param_keys}})
        keys.extend(keys_existed)

        if len(param_keys) > len(keys_existed):
            # get the non-existed key
            param_keys_existed = [key['param_key'] for key in keys_existed]
            param_keys_non_existed = list(set(param_keys) - set(param_keys_existed))
            new_keys = key_service.bulk_create_instances([{"param_key": param_key} for param_key in
                                                          param_keys_non_existed])
            keys.extend(new_keys)

        sorted(keys, key=lambda x: x['param_key'])
        sorted(list_data, key=lambda x: x['param_key'])

        assert len(keys) == len(list_data), "Some wrong with database"

        for i in range(0, len(list_data)):
            del list_data[i]['param_key']
            list_data[i]['key_id'] = keys[i]['_id']

        new_params = self.bulk_create_instances(list_data)
        return new_params

    def create_duplicate_error(self, data_error=None):
        raise InvalidUsage.param_duplicate_error()

    def update_duplicate_error(self, data_error=None):
        raise InvalidUsage.param_duplicate_error()

    def bulk_create_duplicate_error(self, data_error=None):
        param_exists = self.find_param_exist(data_error)
        param_exists = params_schema.dump(param_exists)
        raise InvalidUsage.param_duplicate_error(param_exists)

    def find_param_exist(self, key_value_list):
        keys = [key_value_pair['key_id'] for key_value_pair in key_value_list]
        values = [key_value_pair['param_value'] for key_value_pair in key_value_list]
        param_exist_list = self.get_many_instances({
            "$and": [
                {"key_id": {"$in": keys}},
                {"param_value": {"$in": values}}
            ]
        })
        return param_exist_list


param_service = ParamService()
