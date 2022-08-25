import pymongo

from .models import LastTimeServerStartTest, LastTimeTrackedTest
from datetime import datetime, timedelta
import schedule
import sys


class Controller(object):
    DEFAULT_TIME_SCAN = int(timedelta(seconds=60*2).total_seconds())    # seconds
    TIME_SCAN_MAX = int(timedelta(days=360).total_seconds())
    assert DEFAULT_TIME_SCAN <= TIME_SCAN_MAX, "ERROR: DEFAULT_TIME_SCAN > TIME_SCAN_MAX"

    DEFAULT_TIME_BETWEEN_JOB = int(timedelta(seconds=3).total_seconds())     # seconds
    # If this class variable is not None, time_between_job will use this variable
    FORCE_TIME_BETWEEN_JOB = int(timedelta(seconds=3).total_seconds())

    TIME_START_TRACKING_URL_ACCESS = datetime(2022, 3, 1)       # time start tracking url
    DEFAULT_LAST_TIME_SERVER_START = TIME_START_TRACKING_URL_ACCESS      # time start tracking url
    DEFAULT_LAST_TIME_TRACKED = TIME_START_TRACKING_URL_ACCESS           # time start tracking url

    # This class variable is constructed when this file first be imported
    TIME_CREATE_CONTROLLER_CLASS = datetime.utcnow()

    @classmethod
    def save_time_tracked_and_time_scan(cls, time_job_start, time_scan):
        LastTimeTrackedTest.collection.insert_one({
            LastTimeTrackedTest.last_time_tracked_field: time_job_start,
            LastTimeTrackedTest.time_scan_field: time_scan
        })

    @classmethod
    def save_time_server_start_and_time_between_job(cls, time_server_start, time_between_job=None):
        if time_between_job is None:
            time_between_job = cls.DEFAULT_TIME_BETWEEN_JOB
        LastTimeServerStartTest.collection.insert_one({
            LastTimeServerStartTest.last_time_server_start_field: time_server_start,
            LastTimeServerStartTest.time_between_job_field: time_between_job
        })

    @classmethod
    def get_previous_time_tracked(cls) -> datetime:
        result = LastTimeTrackedTest.collection.\
            find({}, limit=1).\
            sort([
                (LastTimeTrackedTest.last_time_tracked_field, pymongo.DESCENDING)
            ])
        result = list(result)
        if len(result) == 0:
            return cls.DEFAULT_LAST_TIME_TRACKED
        result = result[0]
        return result.get(LastTimeTrackedTest.last_time_tracked_field, cls.DEFAULT_LAST_TIME_TRACKED)

    @classmethod
    def get_last_time_tracked_of_previous_start_session(cls) -> datetime:
        find_result = LastTimeTrackedTest.collection. \
            find({
                LastTimeTrackedTest.last_time_tracked_field: {"$lt": cls.TIME_CREATE_CONTROLLER_CLASS}
            }, limit=1). \
            sort([
                (LastTimeTrackedTest.last_time_tracked_field, pymongo.DESCENDING)
            ])
        find_result = list(find_result)
        if len(find_result) == 0:
            return cls.DEFAULT_LAST_TIME_TRACKED
        last_time_tracked = find_result[0]
        return last_time_tracked.get(LastTimeTrackedTest.last_time_tracked_field, cls.DEFAULT_LAST_TIME_TRACKED)

    @classmethod
    def get_previous_time_server_start(cls) -> datetime:
        result = LastTimeServerStartTest.collection.\
            find({
                LastTimeServerStartTest.last_time_server_start_field: {"$lt": cls.TIME_CREATE_CONTROLLER_CLASS}
            }, limit=1).\
            sort([
                (LastTimeServerStartTest.last_time_server_start_field, pymongo.DESCENDING)
            ])
        result = list(result)
        if len(result) == 0:
            return cls.DEFAULT_LAST_TIME_SERVER_START
        result = result[0]
        return result.get(LastTimeServerStartTest.last_time_server_start_field, cls.DEFAULT_LAST_TIME_SERVER_START)

    @classmethod
    def get_time_between_job_of_previous_start_session(cls):
        result = LastTimeServerStartTest.collection. \
            find({
                LastTimeServerStartTest.last_time_server_start_field: {"$lt": cls.TIME_CREATE_CONTROLLER_CLASS}
            }, limit=1). \
            sort([
                (LastTimeServerStartTest.last_time_server_start_field, pymongo.DESCENDING)
            ])
        result = list(result)
        if len(result) == 0:
            return cls.DEFAULT_TIME_BETWEEN_JOB
        result = result[0]
        return result.get(LastTimeServerStartTest.time_between_job_field, cls.DEFAULT_TIME_BETWEEN_JOB)

    @classmethod
    def save_current_time_between_job(cls, time_between_job):
        LastTimeServerStartTest.collection.update_one(
            {
                LastTimeServerStartTest.last_time_server_start_field: {"$gte": cls.TIME_CREATE_CONTROLLER_CLASS}
            },
            {
                "$set": {
                    LastTimeServerStartTest.time_between_job_field: time_between_job
                }
            }
        )

    @classmethod
    def get_previous_time_scan(cls):
        result = LastTimeTrackedTest.collection.\
            find({}, limit=1).\
            sort([
                (LastTimeTrackedTest.last_time_tracked_field, pymongo.DESCENDING)
            ])
        result = list(result)
        if len(result) == 0:
            return cls.DEFAULT_TIME_SCAN
        result = result[0]
        return result.get(LastTimeTrackedTest.time_scan_field, cls.DEFAULT_TIME_SCAN)

    @classmethod
    def calculate_time_between_job(cls):
        """
        Calculate time_between_job base on previous_time_tracked of previous start session
        """
        last_time_tracked_of_previous_start_session = cls.get_last_time_tracked_of_previous_start_session()

        time_between_job_of_previous_start_session = timedelta(
            seconds=cls.get_time_between_job_of_previous_start_session()
        )

        time_between_job = int(time_between_job_of_previous_start_session.total_seconds())

        if cls.TIME_CREATE_CONTROLLER_CLASS - last_time_tracked_of_previous_start_session <= \
                time_between_job_of_previous_start_session:
            time_between_job = time_between_job_of_previous_start_session / 2
            time_between_job = int(time_between_job.total_seconds())

        if cls.FORCE_TIME_BETWEEN_JOB is not None:
            time_between_job = cls.FORCE_TIME_BETWEEN_JOB

        if time_between_job == 0:
            time_between_job = int(timedelta(seconds=1).total_seconds())

        return time_between_job

    @classmethod
    def create_job(cls):
        time_between_job = cls.calculate_time_between_job()
        cls.save_current_time_between_job(time_between_job)
        from .report_after_time import report_urls_accessed_after
        return schedule.every(time_between_job).seconds.do(report_urls_accessed_after)

