import logging
from google.appengine.api import users
from google.appengine.api import mail
from functools import wraps
from flask import redirect, url_for, request
from .models import User, TemporaryUrl
from config import API_KEY, APP_NAME, EMAIL_WHITELIST


def api_key_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'X-Api-Key' in request.headers.keys():
            if API_KEY == request.headers['X-Api-Key']:
                return f(*args, **kwargs)
        return '', 400

    return decorated_function


def reset_password_email(to):

    # Only send to whitelisted domains
    domain = to.split('@')
    domain = domain[-1]
    
    if not domain.lower() in EMAIL_WHITELIST:
        logging.info('Attempt to send email to unauthorized domain')
        return

    user = User.get_by_id(to)
    if not user:
        logging.info('Attempt to send email to unauthorized user')
        return

    temporay_url = TemporaryUrl()
    temporay_url.user_key = user.key
    temporay_url.put()

    sender = 'lxinventory@{}.appspotmail.com'.format(APP_NAME)
    subject = "Reset Password Link"
    body = "Temporary password reset link: {}".format(temporay_url.url())

    try:
        mail.send_mail(sender=sender, to=to, subject=subject, body=body)
    except Exception as e:
        logging.info("Unable to send email")
        logging.info(e)
    
    return
