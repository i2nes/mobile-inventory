from google.appengine.ext import ndb
from werkzeug.security import generate_password_hash, check_password_hash


class User(ndb.Model):

    id = ndb.StringProperty() # email as id
    name = ndb.StringProperty()
    password = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.key.id()

    def get_key(self):
        return self.key

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        resp = {
            'id': self.key.id(),
            'name': self.name,
        }
        return resp


class Device(ndb.Model):

    inventory_id = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    model = ndb.StringProperty()
    os = ndb.StringProperty()
    user_key = ndb.KeyProperty(kind=User)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    def to_dict(self):
        resp = {
            'user_id': self.user_key.id() if self.user_key is not None else None,
            'username': self.user_key.get().name if self.user_key is not None else None,
            'device_id': self.key.id(),
        }
        return resp