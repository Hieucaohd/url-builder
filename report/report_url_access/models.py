from mongo.base_model import BaseMongoDB


class ReportUrlAccessPerDay(BaseMongoDB):
    meta = {
        'indexes': [
            '-date_string',
            '+url_id',
            {
                "fields": ['-date_string', '+url_id'],
                "unique": True
            }
        ]
    }


class LastTimeTracked(BaseMongoDB):
    meta = {
        'indexes': [
            '-last_time_tracked'
        ]
    }


class LastTimeServerStart(BaseMongoDB):
    meta = {
        'indexes': [
            '-last_time_server_start'
        ]
    }
