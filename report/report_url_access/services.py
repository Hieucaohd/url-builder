from .models import ReportUrlAccessPerDay


class ReportUrlAccessPerDayService(object):
    model = ReportUrlAccessPerDay

    def update_urls_access_count(self, urls_accessed):
        for url_accessed in urls_accessed:
            access_count = url_accessed['access_count']
            del url_accessed['access_count']
            data_update = {
                '$set': {**url_accessed},
                "$inc": {"access_count": access_count}
            }

            condition = {
                "date_string": url_accessed['date_string'],
                "url_id": url_accessed['url_id']
            }

            self.model.collection.update_one(
                condition, data_update, upsert=True
            )


report_url_access_per_day_service = ReportUrlAccessPerDayService()
