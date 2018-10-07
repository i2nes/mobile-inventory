import logging
from google.appengine.api import users
from functools import wraps
from flask import redirect, url_for, request
from .models import User
from config import API_KEY


def api_key_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'X-Api-Key' in request.headers.keys():
            if API_KEY == request.headers['X-Api-Key']:
                return f(*args, **kwargs)
        return '', 400

    return decorated_function