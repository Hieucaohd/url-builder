from .consumer import access_url_consumer
from utils.objectID_convert import convert_to_object_id
from .services import history_access_service
from uaparser import UAParser
from mongo import MongoDBInit
import json


def access_url_receive():
    for data in access_url_consumer:
        message = json.loads(data.value)
        user_agent_string = message.get('user_agent_string', '')
        url_id = message.get('url_id', '')

        user_agent_data = UAParser.parse(user_agent_string)
        user_agent_data['url_id'] = convert_to_object_id(url_id)
        result = history_access_service.create_instance(user_agent_data)
        print(result.get('ua', 'unknown ua') + " saved.")


MongoDBInit.init_client(config={
    'MONGO_URI': "mongodb://localhost:27017",
    'DB_NAME': "devDB"
})
access_url_receive()
