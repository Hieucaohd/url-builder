from base.serializer import BaseSchema
from marshmallow import fields


class ReportUrlAccessPerDaySchema(BaseSchema):
    __envelope_key__ = {'many': 'report_list'}

    _id = fields.Str()
    date_string = fields.Str()
    url_id = fields.Str()
    access_count = fields.Int()


report_url_access_per_day_schema = ReportUrlAccessPerDaySchema(many=True)
