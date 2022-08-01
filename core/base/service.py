from mongo.base_model import BaseMongoDB


class BaseService(object):
    model: BaseMongoDB

    def get_many_instances(self, query, obj_project, page, per_page):
        instances = self.model.objects.find_by_query(query, obj_project, page, per_page)
        return instances

    def get_instance(self, query):
        instance = self.model.objects.find_one(query)
        return instance

    def create_instance(self, **kwargs):
        inserted_id = self.model.objects.insert_one(kwargs)
        return kwargs

    def bulk_create_instances(self, data_list, ignore_invalid_data=True):
        inserted_ids = self.model.objects.bulk_inserts(data_list)
        return inserted_ids

    def update_instance(self, **kwargs):
        pass

    def update_many_instances(self, **kwargs):
        pass

    def get_instance_by_id(self, instance_id, fields):
        instance = self.model.objects.find_one({"_id": instance_id}, fields)
        return instance





