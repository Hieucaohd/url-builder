from mongo.base_model import BaseMongoDB


class Key(BaseMongoDB):
    meta = {
        'indexes': [
            {
                "fields": ["+param_key"],
                "unique": True
            }
        ]
    }


class Param(BaseMongoDB):
    meta = {
        'indexes': [
            {
                "fields": ["+key_id", "+param_value"],
                "unique": True
            }
        ]
    }


class Url(BaseMongoDB):
    meta = {
        'indexes': [
            {
                "fields": ["+param"]
            }
        ]
    }

