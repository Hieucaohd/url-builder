from mongo import MongoDBInit
from datetime import datetime, timedelta


def get_urls_access_between(time_start, time_before=None, unit_and_delta_time=None):
    db_of_history_access = MongoDBInit.get_db('devDB', 'mongodb://localhost:27017')
    history_access_collection = db_of_history_access['historyaccess']

    if time_before is None:
        assert unit_and_delta_time is not None, "must provide timedelta when time_before is None"
        time_before: datetime = time_start - timedelta(**unit_and_delta_time)
    conditions = {
        "$match": {
            "$and": [
                {"created_time": {"$gte": time_before}},
                {"created_time": {"$lt": time_start}},
                {"$or": [
                    {"tracked": False},
                    {"tracked": {"$exists": False}}
                ]}
            ]
        }
    }
    pipeline = [
        conditions,
        {
            "$group": {
                "_id": "$url_id",
                "access_count": {"$count": {}}
            }
        },
        {
            "$project": {
                "_id": 0,
                "url_id": '$_id',
                "access_count": 1,
                'tracking_time': datetime(time_start.year, time_before.month, time_before.day)
            }
        },
    ]
    urls_accessed = history_access_collection.aggregate(pipeline)
    history_access_collection.update_many({
        "$and": [
            {"created_time": {"$gte": time_before}},
            {"created_time": {"$lt": time_start}},
            {"$or": [
                {"tracking": False},
                {"tracking": {"exists": False}}
            ]}
        ]
    }, {
        "$set": {
            "tracking": True
        }
    })
    urls_accessed = list(urls_accessed)
    return urls_accessed


def get_urls_not_tracked():
    db_of_history_access = MongoDBInit.get_db('devDB', 'mongodb://localhost:27017')
    history_access_collection = db_of_history_access['historyaccess']

    time_utc_now = datetime.utcnow()

    conditions = {
        "$or": [
            {"tracked": False},
            {"tracked": {"$exists": False}}
        ]
    }

    pipeline = [
        {
            "$match": conditions
        },
        {
            "$group": {
                "_id": "$url_id",
                "access_count": {"$count": {}}
            }
        },
        {
            "$project": {
                "_id": 0,
                "url_id": '$_id',
                "access_count": 1,
                'tracking_time': datetime(time_utc_now.year, time_utc_now.month, time_utc_now.day)
            }
        }
    ]

    urls_accessed = history_access_collection.aggregate(pipeline)

    history_access_collection.update_many({
        "$and": [
            {**conditions},
            {"created_time": {"$lte": time_utc_now}}
        ]
    }, {
        "$set": {
            'tracked': True
        }
    })
    return list(urls_accessed)
