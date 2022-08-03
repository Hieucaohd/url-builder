import pymongo.errors
import pymongo
from typing import Sequence
from pymongo import IndexModel
from pymongo.collection import Collection


def parse_index_string_config(index_string_config):
    assert type(index_string_config) == str
    index_type = pymongo.ASCENDING
    index_field = index_string_config
    if index_string_config[0] in ['-', '+']:
        index_type = pymongo.ASCENDING if index_string_config[0] == '+' else pymongo.DESCENDING
        index_field = index_string_config[1:]

    return index_field, index_type


def parse_index_config(index_config_raw):

    if type(index_config_raw) == str:
        result = IndexModel(keys=[parse_index_string_config(index_config_raw)], unique=False, background=True)
        return result
    elif type(index_config_raw) == dict:
        assert 'fields' in index_config_raw, f"compound index {index_config_raw} must have fields"
        indexes = [parse_index_string_config(field) for field in index_config_raw['fields']]
        unique = index_config_raw.get("unique", False)
        background = index_config_raw.get("background", True)
        result = IndexModel(keys=indexes, unique=unique, background=background)
        return result

    raise Exception("Invalid indexes syntax.")


def create_mongo_indexes(collection: Collection, indexes):

    assert type(indexes) == list, "Indexes must be list."
    index_configs: Sequence[IndexModel] = []
    for index_config_raw in indexes:
        index_config = parse_index_config(index_config_raw)
        index_configs.append(index_config)

    try:
        collection.create_indexes(index_configs)
    except Exception as e:
        print(f"error={e}")
        print(f"Index {index_configs} failed.")
