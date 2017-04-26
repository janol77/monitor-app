from app.db import db


class Server(db.Document):
    name = db.StringField(required=True)
    ip = db.StringField(required=True)
    description = db.StringField(required=True)
    active = db.BooleanField()
    type_server = db.StringField(required=True)
    deleted = db.BooleanField()
