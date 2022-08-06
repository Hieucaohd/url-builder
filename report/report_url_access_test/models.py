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


class LastTimeTrackedTest(BaseMongoDB):
    meta = {
        'indexes': [
            '-last_time_tracked_field'
        ]
    }

    last_time_tracked_field = 'last_time_tracked_field'
    time_scan_field = 'time_scan_field'


class LastTimeServerStartTest(BaseMongoDB):
    meta = {
        'indexes': [
            '-last_time_server_start_field'
        ]
    }

    last_time_server_start_field = 'last_time_server_start_field'
    time_between_job_field = "time_between_job_field"
