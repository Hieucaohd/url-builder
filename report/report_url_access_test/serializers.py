from base import BaseSchema
from marshmallow import fields


class UrlAccessPerDaySchema(BaseSchema):
    url_id = fields.Str()
    access_count = fields.Number()
    date_string = fields.Str()


url_access_per_day_schema = UrlAccessPerDaySchema()
