from flask import Blueprint, request
from utils.docs_register import register_view
from .kafka_config import ACCESS_URL_TOPIC
from .producer import access_url_producer
import json

blueprint = Blueprint('history_access', __name__)


@blueprint.route('/access/url/<url_id>', methods=('GET',))
def access_url(url_id):
    user_agent_string = request.headers.get('User-Agent')
    data = {
        "user_agent_string": user_agent_string,
        "url_id": url_id
    }
    data = json.dumps(data)
    access_url_producer.send(ACCESS_URL_TOPIC, value=data)
    return 'oke'


def register_docs(docs):
    register_view(docs, blueprint, [
        access_url
    ])

