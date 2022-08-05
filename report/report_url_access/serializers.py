from base import BaseSchema
from marshmallow import fields


class UrlAccessPerDaySchema(BaseSchema):
    datetime = fields.DateTime()
    url_id = fields.Str()
    access_count = fields.Number()
    tracking = fields.Boolean()


url_access_per_day_schema = UrlAccessPerDaySchema()
