from mongo import MongoDBInit
import schedule
from report import report_url_access

MongoDBInit.init_client(config={
    'MONGO_URI': "mongodb://localhost:27017",
    'DB_NAME': "devDB"
})

report_url_access.main()

while True:
    schedule.run_pending()
