from flask import Blueprint, request
from utils.docs_register import register_view
from common.constant import ACCESS_URL_TOPIC
import json
from kafka import KafkaProducer

blueprint = Blueprint('history_access', __name__)


@blueprint.route('/access/url/<url_id>', methods=('GET',))
def access_url(url_id):
    user_agent_string = request.headers.get('User-Agent')
    data = {
        "user_agent_string": user_agent_string,
        "url_id": url_id
    }
    data = json.dumps(data)
    access_url_producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: x.encode('utf-8')
    )
    access_url_producer.send(ACCESS_URL_TOPIC, value=data)
    return 'oke'


def register_docs(docs):
    register_view(docs, blueprint, [
        access_url
    ])

