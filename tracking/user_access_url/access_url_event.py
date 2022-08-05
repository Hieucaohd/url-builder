from .consumer import access_url_consumer
from utils.objectID_convert import convert_to_object_id
from .services import history_access_service
from uaparser import UAParser
import json
from datetime import datetime
from common.constant import DATE_FORMAT_STRING


def access_url_receive_consumer():
    for data in access_url_consumer:
        message = json.loads(data.value)
        user_agent_string = message.get('user_agent_string', '')
        url_id = message.get('url_id', '')

        user_agent_data = UAParser.parse(user_agent_string)

        user_agent_data['url_id'] = convert_to_object_id(url_id)
        user_agent_data['date_string'] = datetime.utcnow().date().strftime(DATE_FORMAT_STRING)
        # user_agent_data['date_string'] = '2022/08/04'

        result = history_access_service.create_instance(user_agent_data)

        print(result.get('ua', 'unknown ua') + " saved.")


