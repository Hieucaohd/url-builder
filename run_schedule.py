from mongo import MongoDBInit
import schedule
from report.report_url_access import get_urls_not_tracked

MongoDBInit.init_client(config={
    'MONGO_URI': "mongodb://localhost:27017",
    'DB_NAME': "devDB"
})

get_urls_not_tracked()

