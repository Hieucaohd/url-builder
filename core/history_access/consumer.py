import json
from kafka import KafkaConsumer
from .kafka_config import ACCESS_URL_TOPIC


access_url_consumer = KafkaConsumer(
    ACCESS_URL_TOPIC,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='receive-access-url-event',
    value_deserializer=lambda x: x.decode('utf-8')
)
