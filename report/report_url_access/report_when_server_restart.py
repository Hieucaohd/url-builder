from datetime import datetime, timedelta
import pymongo
from .history_access_service import get_urls_access_between
from .controller import Controller
from .services import report_url_access_per_day_service


def report_urls_accessed_while_server_stop():
    """
    TODO: if (time_start - previous_time_tracked) too much large, let scale this function
    """
    time_start = datetime.utcnow()

    last_time_tracked_of_previous_start_session = Controller.get_last_time_tracked_of_previous_start_session()

    Controller.save_time_tracked(time_start)

    urls_accessed = get_urls_access_between(time_start, last_time_tracked_of_previous_start_session)
    report_url_access_per_day_service.update_urls_access_count(urls_accessed)
