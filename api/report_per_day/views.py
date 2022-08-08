from flask import Blueprint
from flask_apispec import marshal_with
from .serializers import report_url_access_per_day_schema
from .services import report_url_access_per_day_service
from utils.docs_register import register_view
from datetime import datetime
from common.constant import DATE_FORMAT_STRING


blueprint = Blueprint('report_per_day', __name__)


@blueprint.route('/api/report_per_days/in_date/<date>', methods=('GET',))
@marshal_with(report_url_access_per_day_schema)
def get_report_in_day(date: str):
    date = datetime.strptime(date, "%d-%m-%Y")
    date = date.date().strftime(DATE_FORMAT_STRING)
    reports = report_url_access_per_day_service.get_report_in_day(date=date)
    return reports


@blueprint.route('/api/report_per_days/of_url/<url_id>', methods=['GET'])
@marshal_with(report_url_access_per_day_schema)
def get_report_of_url(url_id):
    reports = report_url_access_per_day_service.get_report_of_url(url_id)
    return reports


def register_docs(docs):
    register_view(docs, blueprint, [
        get_report_in_day,
        get_report_of_url
    ])
