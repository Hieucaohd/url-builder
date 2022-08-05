from mongo.base_model import BaseMongoDB


class HistoryAccess(BaseMongoDB):
    meta = {
        'indexes': [
            '+url_id',
            '-created_time',
            '-tracked'
        ],
        'auto_timestamp': True
    }
