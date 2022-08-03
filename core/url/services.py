from .models import Url
from core.base import BaseService
from utils.objectID_convert import convert_to_object_id
from core.param_key.models import Key
from core.param.models import Param
from core.param.services import param_service


class UrlService(BaseService):
    model = Url

    def quick_create_url(self, data, ignore_invalid_data=True):

        params = []
        params_input = data['param_list']
        key_collection_name = Key.COLLECTION_NAME

        params_existed = []
        for param_input in params_input:
            pipeline = [
                {
                    "$lookup": {
                        "from": key_collection_name,
                        "localField": 'key_id',
                        "foreignField": '_id',
                        "as": 'keys'
                    }
                },
                {
                    "$project": {
                        "_id": 1,
                        "param_key": {"$first": "$keys.param_key"},
                        "param_value": 1
                    }
                },
                {
                    "$match": {
                        "$and": [
                            {"param_key": param_input['param_key']},
                            {"param_value": param_input['param_value']}
                        ]
                    }
                }
            ]
            param_existed = list(Param.collection.aggregate(pipeline))
            if len(param_existed) > 0:
                params_existed.append(param_existed[0])

        params.extend(params_existed)

        if len(params_input) > len(list(params_existed)):
            params_non_existed = []
            for param in params_input:
                take = True
                for param_existed in params_existed:
                    if param['param_key'] == param_existed['param_key'] and\
                            param['param_value'] == param_existed['param_value']:
                        take = False
                        break
                if take:
                    params_non_existed.append(param)

            params_non_existed_created = param_service.quick_bulk_create_params(params_non_existed)
            params.extend(params_non_existed_created)

        data['param_ids'] = [param['_id'] for param in params]
        del data['param_list']

        new_url = self.create_instance(data)

        return new_url

    def get_url_string(self, url_id):
        url_id_string = url_id
        url_id = convert_to_object_id(url_id)
        key_collection_name = Key.COLLECTION_NAME
        param_collection_name = Param.COLLECTION_NAME
        pipeline = [
            {
                "$lookup": {
                    "from": param_collection_name,
                    "localField": 'param_ids',
                    "foreignField": '_id',
                    "as": "params"
                }
            },
            {
                "$match": {
                    "_id": url_id
                }
            },
            {
                "$project": {
                    '_id': 0,
                    'params': 1
                }
            },
            {
                "$lookup": {
                    "from": key_collection_name,
                    "localField": "params.key_id",
                    "foreignField": "_id",
                    "as": 'keys'
                }
            }
        ]
        result = self.model.collection.aggregate(pipeline)
        result = list(result)

        if len(result) == 0:
            return ''

        result = result[0]

        keys = result['keys']
        params = result['params']

        key_value_pairs = []

        for param in params:
            for key in keys:
                if param['key_id'] == key['_id']:
                    key_value_pairs.append({'param_key': key['param_key'], 'param_value': param['param_value']})
                    break

        url_string = f'http://127.0.0.1:5000/access/url/{url_id_string}?'
        for key_value_pair in key_value_pairs[:-1]:
            url_string = url_string + key_value_pair['param_key'] + '=' + key_value_pair['param_value'] + '&'

        url_string = url_string + key_value_pairs[-1]['param_key'] + '=' + key_value_pairs[-1]['param_value']

        return url_string


url_service = UrlService()
