from mongo import MongoDBInit
from datetime import timedelta


def get_urls_access_between(time_start, time_end=None, after_time=None):
    db_of_history_access = MongoDBInit.get_db('devDB', 'mongodb://localhost:27017')
    history_access_collection = db_of_history_access['historyaccess']

    if time_end is None:
        assert after_time is not None, "you must provide after_time when time_end is not provide"
        time_end = time_start - timedelta(seconds=after_time)

    conditions = {
        "$and": [
            {"created_time": {"$gte": time_end}},
            {"created_time": {"$lt": time_start}}
        ]
    }
    pipeline = [
        {
            "$match": conditions
        },
        {
            "$group": {
                "_id": {
                    "date_string": "$date_string",
                    "url_id": "$url_id"
                },
                "access_count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "url_id": '$_id.url_id',
                "access_count": 1,
                "date_string": "$_id.date_string"
            }
        },
        {
            "$sort": {"date_string": -1}
        }
    ]
    urls_accessed = history_access_collection.aggregate(pipeline)
    urls_accessed = list(urls_accessed)
    return urls_accessed
