from mongo import MongoDBInit
import schedule
from report.report_url_access import report_urls_accessed_after, report_urls_accessed_while_server_stop, Controller

MongoDBInit.init_client(config={
    'MONGO_URI': "mongodb://localhost:27017",
    'DB_NAME': "devDB"
})

report_urls_accessed_while_server_stop()
schedule.every(30).seconds.do(report_urls_accessed_after, after_time=Controller.DEFAULT_TIME_GET_REPORT)

while True:
    schedule.run_pending()
