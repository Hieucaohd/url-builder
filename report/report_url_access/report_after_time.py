from datetime import datetime
from .history_access_service import get_urls_access_between
from .services import report_url_access_per_day_service
from .controller import Controller


def report_urls_accessed_after(after_time):
    time_utc_now = datetime.utcnow()
    Controller.save_last_time_tracked(time_utc_now)

    urls_accessed = get_urls_access_between(time_utc_now, after_time=after_time)

    report_url_access_per_day_service.update_urls_access_count(urls_accessed)
