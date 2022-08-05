from datetime import datetime, timedelta

import pymongo

from .history_access_service import get_urls_access_between
from .models import ReportUrlAccessPerDay
from .controller import Controller
from .services import report_url_access_per_day_service


def report_urls_accessed_while_server_stop():
    time_utc_now = datetime.utcnow()

    last_time_tracked = Controller.get_last_time_tracked()

    Controller.save_last_time_server_start(time_utc_now)
    Controller.save_last_time_tracked(time_utc_now)

    urls_accessed = get_urls_access_between(time_utc_now, last_time_tracked)
    report_url_access_per_day_service.update_urls_access_count(urls_accessed)
