from app.db import db
from werkzeug import generate_password_hash
from libs.tools import code_generator


class User(db.Document):
    name = db.StringField(required=True)
    state = db.StringField(required=True)
    code = db.StringField(required=True)
    active = db.BooleanField(required=True, default=True)
    password = db.StringField()
    email = db.StringField(required=True)
    rol = db.StringField(required=True)
    protected = db.BooleanField(required=True, default=False)
    deleted = db.BooleanField(required=True, default=False)

    def generate_password(self):
        """Calculate the password."""
        self.password = generate_password_hash(self.password)

    def generate_code(self):
        """Calculate the password."""
        self.code = code_generator(size=30, hexdigits=True)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id.__str__()

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
