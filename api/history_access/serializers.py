from marshmallow import Schema, fields


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
    model = fields.Str(required=False)
    type = fields.Str(required=False)
    vendor = fields.Str(required=False)


class CPUSchema(Schema):
    architecture = fields.Str()


class HistoryAccessUrlSchema(Schema):
    __envelope_key__ = {'single': 'history_access'}

    _id = fields.UUID(dump_only=True)
    url_id = fields.Str()
    ua = fields.Str()
    browser = fields.Nested(BrowserSchema, required=False)
    engine = fields.Nested(EngineSchema)
    os = fields.Nested(OsSchema)
    device = fields.Nested(DeviceSchema, required=False)
    cpu = fields.Nested(CPUSchema)
    accessed_time = fields.DateTime()


history_access_schema = HistoryAccessUrlSchema()
