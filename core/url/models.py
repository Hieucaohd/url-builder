import mongoengine as me
from datetime import datetime


class Key(me.Document):
    key_id = me.ObjectIdField(primary_key=True)
    param_key = me.StringField(required=True)
    created_time = me.DateTimeField(default=datetime.utcnow())

    meta = {
        'indexes': [
            {
                "fields": ['key_id'],
                "unique": True
            },
            {
                "fields": ["param_key"],
                "unique": True
            }
        ]
    }


class Param(me.Document):
    param_id = me.ObjectIdField(primary_key=True)
    key_id = me.ReferenceField(Key, required=True)
    param_value = me.StringField(required=True)
    created_time = me.DateTimeField(default=datetime.utcnow())
    updated_time = me.DateTimeField(default=datetime.utcnow())

    meta = {
        'indexes': [
            {
                "fields": ["param_id"],
                "unique": True
            },
            {
                "fields": ["key_id", "param_value"],
                "unique": True
            }
        ]
    }


class Url(me.Document):
    url_id = me.ObjectIdField(primary_key=True)
    name = me.StringField()
    params = me.ListField(me.ReferenceField(Param))
    created_time = me.DateTimeField(default=datetime.utcnow())
    updated_time = me.DateTimeField(default=datetime.utcnow())

    meta = {
        'indexes': [
            {
                'fields': ['url_id'],
                'unique': True
            },
            {
                'fields': ['params'],
                'unique': True
            }
        ]
    }

