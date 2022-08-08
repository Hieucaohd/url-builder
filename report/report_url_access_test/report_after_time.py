from datetime import datetime, timedelta
from .history_access_service import get_urls_access_between
from .services import report_url_access_per_day_service
from .controller import Controller
import sys


def calculate_time_scan(time_utc_now: datetime, previous_time_tracked: datetime) -> timedelta:
    time_scan = timedelta(seconds=Controller.get_previous_time_scan())
    time_scan_max = timedelta(seconds=Controller.TIME_SCAN_MAX)
    if time_utc_now - previous_time_tracked > 2 * time_scan:
        time_scan = time_scan * 2

    if time_scan > time_scan_max:
        time_scan = time_scan_max

    if time_scan + previous_time_tracked > time_utc_now:
        time_scan = time_utc_now - previous_time_tracked

    return time_scan


def report_urls_accessed_after():
    time_utc_now = datetime.utcnow()
    previous_time_tracked = Controller.get_previous_time_tracked()
    time_scan = calculate_time_scan(time_utc_now, previous_time_tracked)

    timeline_tracked = previous_time_tracked + time_scan

    Controller.save_time_tracked_and_time_scan(timeline_tracked, time_scan.total_seconds())

    urls_accessed = get_urls_access_between(timeline_tracked, previous_time_tracked)

    report_url_access_per_day_service.update_urls_access_count(urls_accessed)

    print(f"\nComplete scan to report from {previous_time_tracked} to {timeline_tracked}, scan results: {urls_accessed}")
