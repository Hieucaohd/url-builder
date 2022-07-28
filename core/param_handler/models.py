import mongoengine as me
from datetime import datetime


class Key(me.Document):
    param_key = me.StringField(required=True)
    created_time = me.DateTimeField(default=datetime.utcnow())

    meta = {
        "auto_create_index": False,
        "index_background": True,
        'indexes': [
            {
                "fields": ["param_key"],
                "unique": True,
            },
        ]
    }

    def __repr__(self):
        return '<Key(param_key={self.param_key!r})>'.format(self=self)


class Param(me.Document):
    key_id = me.ReferenceField(Key, required=True)
    param_value = me.StringField(required=True)
    created_time = me.DateTimeField(default=datetime.utcnow())
    updated_time = me.DateTimeField(default=datetime.utcnow())

    meta = {
        "auto_create_index": False,
        "index_background": True,
        'indexes': [
            {
                "fields": ["key_id", "param_value"],
                "unique": True
            }
        ]
    }

    def __repr__(self):
        return '<Key(name={self.key_id!r})>'.format(self=self)


class Url(me.Document):
    name = me.StringField()
    params = me.ListField(me.ReferenceField(Param))
    created_time = me.DateTimeField(default=datetime.utcnow())
    updated_time = me.DateTimeField(default=datetime.utcnow())

    meta = {
        "auto_create_index": False,
        "index_background": True,
        'indexes': [
            {
                'fields': ['params'],
                'unique': True
            }
        ]
    }

