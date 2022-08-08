from flask import Blueprint, request
from .services import test_performance_service


blueprint = Blueprint('test_performance', __name__)


@blueprint.route('/test_performance/empty_get', methods=['GET'])
def empty_get():
    return 'oke'


@blueprint.route('/test_performance/empty_post', methods=['POST'])
def empty_post():
    return 'oke'


@blueprint.route('/test_performance/insert_sync', methods=['POST'])
def insert_sync():
    data = request.json
    test_performance_service.insert_one(data)
    return 'ok'
