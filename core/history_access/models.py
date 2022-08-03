from mongo.base_model import BaseMongoDB


class HistoryAccess(BaseMongoDB):
    meta = {
        'indexes': [
            '+url_id'
        ],
        'auto_timestamp': True
    }
