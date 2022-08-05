from mongo.base_model import BaseMongoDB


class Param(BaseMongoDB):
    meta = {
        'indexes': [
            {
                "fields": ["+key_id", "+param_value"],
                "unique": True
            }
        ],
        'auto_timestamp': True
    }
