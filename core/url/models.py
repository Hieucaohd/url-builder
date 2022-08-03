from mongo.base_model import BaseMongoDB


class Url(BaseMongoDB):
    meta = {
        'indexes': [
            {
                "fields": ["+param"]
            }
        ],
        'auto_timestamp': True
    }
