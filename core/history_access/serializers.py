from marshmallow_mongoengine import ModelSchema
from .models import HistoryAccessUrl


class HistoryAccessSchema(ModelSchema):
    class Meta:
        model = HistoryAccessUrl


history_access_schema = HistoryAccessSchema()
