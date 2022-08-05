from base import BaseService
from .models import HistoryAccess


class HistoryAccessService(BaseService):
    model = HistoryAccess


history_access_service = HistoryAccessService()
