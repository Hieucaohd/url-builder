from tracking.user_access_url.access_url_event import access_url_receive_consumer
from mongo import MongoDBInit


MongoDBInit.init_client(config={
    'MONGO_URI': "mongodb://localhost:27017",
    'DB_NAME': "devDB"
})
access_url_receive_consumer()
