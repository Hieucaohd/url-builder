from mongo.base_model import BaseMongoDB


class Key(BaseMongoDB):
    meta = {
        'indexes': [
            {
                "fields": ["+param_key"],
                "unique": True
            }
        ],
        'auto_timestamp': True
    }
