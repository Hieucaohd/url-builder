from mongo.base_model import BaseMongoDB


class ReportUrlAccessPerDayTest(BaseMongoDB):
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

    date_string_field = 'date_string'
    access_count_field = 'access_count'
    url_id_field = 'url_id'


class LastTimeTrackedTest(BaseMongoDB):
    meta = {
        'indexes': [
            '-last_time_tracked'
        ]
    }

    last_time_tracked_field = 'last_time_tracked'
    time_scan_field = 'time_scan'


class LastTimeServerStartTest(BaseMongoDB):
    meta = {
        'indexes': [
            '-last_time_server_start'
        ]
    }

    last_time_server_start_field = 'last_time_server_start'
    time_between_job_field = "time_between_job"
