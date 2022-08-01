from marshmallow import Schema, fields
from core.base.serializer import BaseSchema
from core.param_handler.serializers import UrlSchema
from datetime import datetime


class BrowserSchema(Schema):
    name = fields.Str()
    version = fields.Str()
    major = fields.Str()


class EngineSchema(Schema):
    name = fields.Str()
    version = fields.Str()


class OsSchema(Schema):
    name = fields.Str()
    version = fields.Str()


class DeviceSchema(Schema):
    model = fields.Str()
    type = fields.Str()
    vendor = fields.Str()


class CPUSchema(Schema):
    architecture = fields.Str()


class HistoryAccessUrlSchema(BaseSchema):
    id = fields.UUID(dump_only=True)
    url = fields.Nested(UrlSchema)
    ua = fields.Str(required=True)
    browser = fields.Nested(BrowserSchema)
    engine = fields.Nested(EngineSchema)
    os = fields.Nested(OsSchema)
    device = fields.Nested(DeviceSchema)
    cpu = fields.Nested(CPUSchema)
    accessed_time = fields.DateTime(default=datetime.utcnow())


history_access_schema = HistoryAccessUrlSchema()
