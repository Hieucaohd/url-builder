from base import BaseService
from . models import ReportUrlAccessPerDay


class UrlAccessPerDayService(BaseService):
    model = ReportUrlAccessPerDay


url_access_per_day_service = UrlAccessPerDayService()
