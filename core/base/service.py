

class BaseService(object):
    model = None

    def get_instance_by_id(self, instance_id):
        instance = self.get_instance(id=instance_id)
        return instance

    def create_instance(self, **kwargs):
        new_instance = self.model(**kwargs)
        return new_instance.save()

    def bulk_create_instance(self, **kwargs):
        pass

    def get_instance(self, **kwargs):
        instance = self.model.objects(**kwargs).first()
        return instance

    def get_many_instances(self, limit=10, skip=0, order_by="", **kwargs):
        instances = self.model.objects(**kwargs).limit(limit).skip(skip).order_by(order_by)
        return instances

    def update_instance(self, **kwargs):
        pass

    def update_many_instances(self, **kwargs):
        pass
