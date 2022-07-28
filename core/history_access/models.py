import mongoengine as me
from datetime import datetime
from core.param_handler import models as url_models


class Browser(me.EmbeddedDocument):
    name = me.StringField()
    version = me.StringField()
    major = me.StringField()


class Engine(me.EmbeddedDocument):
    name = me.StringField()
    version = me.StringField()


class OS(me.EmbeddedDocument):
    name = me.StringField()
    version = me.StringField()


class Device(me.EmbeddedDocument):
    model = me.StringField()
    type = me.StringField()
    vendor = me.StringField()


class CPU(me.EmbeddedDocument):
    architecture = me.StringField()


class HistoryAccessUrl(me.Document):
    url_id = me.ReferenceField(url_models.Url)
    ua = me.StringField(required=True)
    browser = me.EmbeddedDocument(Browser)
    engine = me.EmbeddedDocumentField(Engine)
    os = me.EmbeddedDocumentField(OS)
    device = me.EmbeddedDocumentField(Device)
    cpu = me.EmbeddedDocumentField(CPU)
    accessed_time = me.DateTimeField(default=datetime.utcnow())

    meta = {
        "indexes": ['url_id']
    }
