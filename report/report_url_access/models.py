from mongo.base_model import BaseMongoDB


class ReportUrlAccessPerDay(BaseMongoDB):
    meta = {
        'indexes': [
            '-tracking_time',
            '+url_id'
        ]
    }
