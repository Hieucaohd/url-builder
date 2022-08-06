from datetime import datetime, timedelta
from .history_access_service import get_urls_access_between
from .services import report_url_access_per_day_service
from .controller import Controller
import sys


def calculate_time_scan(time_utc_now, last_time_tracked):
    time_scan = timedelta(seconds=Controller.get_previous_time_scan())
    if time_utc_now - last_time_tracked > 2 * time_scan:
        time_scan = time_scan + timedelta(seconds=3*60)

    if time_scan > Controller.TIME_SCAN_MAX:
        time_scan = Controller.TIME_SCAN_MAX

    if time_scan + last_time_tracked > time_utc_now:
        time_scan = time_utc_now - last_time_tracked

    return time_scan


def report_urls_accessed_after():
    time_utc_now = datetime.utcnow()
    last_time_tracked = Controller.get_previous_time_tracked()
    time_scan = calculate_time_scan(time_utc_now, last_time_tracked)

    timeline_tracked = last_time_tracked + time_scan

    if timeline_tracked > time_utc_now:
        print("WARNING: timeline_tracked > time_utc_now")
        sys.exit(1)

    Controller.save_time_tracked_and_time_scan(timeline_tracked, time_scan)

    urls_accessed = get_urls_access_between(timeline_tracked, last_time_tracked)

    report_url_access_per_day_service.update_urls_access_count(urls_accessed)

    print(f"\nComplete scan to report from {last_time_tracked} to {timeline_tracked}, scan all: {urls_accessed}")
