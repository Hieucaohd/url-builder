from base import BaseService
from datetime import datetime
from .models import HistoryAccess


class HistoryAccessService(object):
    model = HistoryAccess

    def insert_one(self, data):
        data['created_time'] = datetime.utcnow()
        inserted_id = self.model.collection.insert_one(data)
        data['_id'] = inserted_id
        return data


history_access_service = HistoryAccessService()
