import pymongo

from .models import LastTimeServerStart, LastTimeTracked
from datetime import datetime


class Controller(object):
    DEFAULT_TIME_GET_REPORT = {"seconds": 30}
    DEFAULT_SERVER_START = datetime(2002, 2, 19)
    DEFAULT_JOB_START = datetime(2002, 2, 19)

    @classmethod
    def save_last_time_tracked(cls, time_job_start):
        LastTimeTracked.collection.insert_one({
            "last_time_tracked": time_job_start
        })

    @classmethod
    def save_last_time_server_start(cls, time_server_start):
        LastTimeServerStart.collection.insert_one({
            "last_time_server_start": time_server_start
        })

    @classmethod
    def get_last_time_tracked(cls) -> datetime:
        result = LastTimeTracked.collection.find({}, limit=1).sort([('last_time_tracked', pymongo.DESCENDING)])
        result = list(result)
        if len(result) == 0:
            return cls.DEFAULT_JOB_START
        result = result[0]
        return result['last_time_tracked']

    @classmethod
    def get_last_time_server_start(cls) -> datetime:
        result = LastTimeServerStart.collection.find({}, limit=1).sort([('last_time_server_start', pymongo.DESCENDING)])
        result = list(result)
        if len(result) == 0:
            return cls.DEFAULT_SERVER_START
        result = result[0]
        return result['last_time_server_start']

