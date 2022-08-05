from mongo.base_model import BaseMongoDB
from datetime import datetime
from pymongo import ReturnDocument
from utils.objectID_convert import convert_to_object_id
import pymongo.errors
from abc import ABC, abstractmethod


def add_create_timestamp(data: dict):
    data['created_time'] = datetime.utcnow()
    data['updated_time'] = data['created_time']
    return data


def add_update_timestamp(data: dict):
    data['updated_time'] = datetime.utcnow()
    return data


def auto_create_timestamp(model):
    model_meta = getattr(model, "meta", {})
    auto_add_timestamp = model_meta.get("auto_timestamp", False)
    return auto_add_timestamp


class BaseService(object):
    model: BaseMongoDB

    def get_many_instances(self, query={}, obj_project=None, page=None, per_page=None, sort=None):
        instances = self.model.objects.find_by_query(query, obj_project, page, per_page, sort)
        return instances

    def get_instance(self, query):
        instance = self.model.objects.find_one(query)
        return instance

    def create_instance(self, data):
        if auto_create_timestamp(self.model):
            add_create_timestamp(data)

        inserted_id = self.model.objects.insert_one(data)
        data['_id'] = inserted_id

        return data

    def bulk_create_instances(self, data_list, ignore_invalid_data=True):
        if auto_create_timestamp(self.model):
            for data in data_list:
                add_create_timestamp(data)

        inserted_ids = self.model.objects.bulk_inserts(data_list)
        for i in range(0, len(data_list)):
            data_list[i]['_id'] = inserted_ids[i]
        return data_list

    def update_instance(self, query, data):
        if auto_create_timestamp(self.model):
            add_update_timestamp(data)
        updated_instance = self.model.objects.find_one_and_update(query, data, return_document=ReturnDocument.AFTER)
        return updated_instance

    def find_one_and_update(self, query, data, return_document=ReturnDocument.AFTER, upsert=False):
        if auto_create_timestamp(self.model):
            add_update_timestamp(data)
        updated_instance = self.model.objects.find_one_and_update(query, data, return_document, upsert)
        return updated_instance

    def update_instance_by_id(self, instance_id, data):
        instance_id = convert_to_object_id(instance_id)
        updated_instance = self.update_instance({"_id": instance_id}, data)
        return updated_instance

    def get_instance_by_id(self, instance_id, fields=None):
        instance_id = convert_to_object_id(instance_id)
        instance = self.model.objects.find_one({"_id": instance_id}, fields)
        return instance

    def delete_instance(self, query):
        return self.model.objects.delete_one(query)

    def delete_instance_by_id(self, instance_id):
        instance_id = convert_to_object_id(instance_id)
        return self.delete_instance({"_id": instance_id})


class KeyUniqueBaseService(BaseService, ABC):
    def create_instance(self, data):
        try:
            instance = super().create_instance(data)
            return instance
        except pymongo.errors.DuplicateKeyError as e:
            return self.create_duplicate_error(data)

    def bulk_create_instances(self, data_list: list, ignore_invalid_data=True):
        try:
            instances = super().bulk_create_instances(data_list, ignore_invalid_data=ignore_invalid_data)
            return instances
        except pymongo.errors.BulkWriteError as e:
            return self.bulk_create_duplicate_error(data_list)

    def update_instance(self, query, data):
        try:
            updated_instance = super().update_instance(query, data)
            return updated_instance
        except pymongo.errors.DuplicateKeyError as e:
            return self.update_duplicate_error(data)
            # raise InvalidUsage.param_key_duplicate_error()

    @abstractmethod
    def create_duplicate_error(self, data_error=None):
        pass

    @abstractmethod
    def bulk_create_duplicate_error(self, data_error=None):
        pass

    @abstractmethod
    def update_duplicate_error(self, data_error=None):
        pass

