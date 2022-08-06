from datetime import datetime, timedelta
from .history_access_service import get_urls_access_between
from .services import report_url_access_per_day_service
from .controller import Controller
import sys


def calculate_timeline_tracked(time_utc_now, last_time_tracked):
    """
    TODO: replace me
    """
    return time_utc_now


def report_urls_accessed_after():
    time_utc_now = datetime.utcnow()
    last_time_tracked = Controller.get_last_time_tracked()
    timeline_tracked = calculate_timeline_tracked(time_utc_now, last_time_tracked)

    if timeline_tracked > time_utc_now:
        print("WARNING: timeline_tracked > time_utc_now")
        sys.exit(1)

    Controller.save_time_tracked(timeline_tracked)

    urls_accessed = get_urls_access_between(timeline_tracked, last_time_tracked)

    report_url_access_per_day_service.update_urls_access_count(urls_accessed)

    print(f"\nComplete scan to report from {last_time_tracked} to {timeline_tracked}, scan all: {urls_accessed}")
