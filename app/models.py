from google.appengine.ext import ndb


class User(ndb.Model):

    name = ndb.StringProperty()
    email = ndb.StringProperty()
    authorized = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

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