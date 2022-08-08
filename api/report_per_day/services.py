from .models import ReportUrlAccessPerDay
from utils.objectID_convert import convert_to_object_id


class ReportUrlAccessPerDayService(object):
    model = ReportUrlAccessPerDay

    def get_report_in_day(self, date):
        reports = self.model.collection.find({"date_string": date})
        return list(reports)

    def get_report_of_url(self, url_id):
        url_id = convert_to_object_id(url_id)
        reports = self.model.collection.find({"url_id": url_id})
        return list(reports)


report_url_access_per_day_service = ReportUrlAccessPerDayService()
