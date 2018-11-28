from google.appengine.ext import ndb
from werkzeug.security import generate_password_hash, check_password_hash
from config import APP_NAME
from datetime import datetime


class User(ndb.Model):

    name = ndb.StringProperty()
    password = ndb.StringProperty()
    isAdmin = ndb.BooleanProperty(default=False)
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
    
    def is_admin(self):
        return self.isAdmin

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

    manufacturer = ndb.StringProperty()
    model = ndb.StringProperty()
    os = ndb.StringProperty()
    availability = ndb.BooleanProperty(default=True)
    lockModelName = ndb.BooleanProperty(default=False)
    user_key = ndb.KeyProperty(kind=User)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    def isLockedModelName(self):
        return self.lockModelName

    def to_dict(self):
        resp = {
            'user_id': self.user_key.id() if self.user_key is not None else None,
            'username': self.user_key.get().name if self.user_key is not None else None,
            'device_id': self.key.id(),
        }
        return resp


class DeviceTransaction(ndb.Model):

    device_key = ndb.KeyProperty(kind=Device)
    user_key = ndb.KeyProperty(kind=User)
    operation = ndb.StringProperty()
    transaction_date = ndb.DateTimeProperty(auto_now_add=True)


class TemporaryUrl(ndb.Model):

    user_key = ndb.KeyProperty(kind=User)
    created = ndb.DateTimeProperty(auto_now_add=True)
    isValid = ndb.BooleanProperty(default=True)
    
    def url(self):
        return "https://{}.appspot.com/resetpassword/{}".format(APP_NAME, str(self.key.id()))
    
    def isActive(self):
        delta = datetime.now() - self.created
        return self.isValid and int(delta.total_seconds()) < 3600 # Link older than 60 minutes
