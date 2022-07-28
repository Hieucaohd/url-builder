from .models import Key
from core.base import BaseService


class KeyService(BaseService):
    model = Key


key_service = KeyService()
