from datetime import datetime
from .history_access_service import get_urls_not_tracked
from .models import ReportUrlAccessPerDay


def report_urls_accessed_while_server_stop():
    time_utc_now = datetime.utcnow()
    urls_accessed = get_urls_not_tracked()
    for url_accessed in urls_accessed:
        data = {
            "$set": {**url_accessed},
            "$inc": {"access_count": url_accessed['access_count']}
        }
        result = ReportUrlAccessPerDay.collection.update_one({
            "url_id": url_accessed['url_id'],
            "tracking_time": datetime(time_utc_now.year, time_utc_now.month, time_utc_now.day)
        }, data, upsert=True)
        print(result)
