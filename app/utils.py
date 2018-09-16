import logging
from google.appengine.api import users
from functools import wraps
from flask import redirect, url_for, request
from .models import User
from config import API_KEY


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        user = users.get_current_user()
        if user is None:
            return redirect(url_for('web_app.home_page'))
        else:
            q = User.query(User.email == user.email())
            user_ndb = q.fetch()
            if user_ndb:
                if user_ndb[0].authorized == True:
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for('web_app.home_page'))
            else:
                logging.info(len(User.query().fetch()))
                new_user = User()
                new_user.email = user.email()
                if len(User.query().fetch()) == 0:
                    new_user.authorized = True
                new_user.put()
                logging.info("Created a new user: {}".format(user.email()))
                return redirect(url_for('web_app.home_page'))

    return decorated_function


def api_key_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'X-Api-Key' in request.headers.keys():
            if API_KEY == request.headers['X-Api-Key']:
                return f(*args, **kwargs)
        return '', 400

    return decorated_function