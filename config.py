# Flask App Configurations
import os
from socket import gethostname
from google.appengine.api import users


config = {
    'DEBUG': True if os.getenv('SERVER_SOFTWARE', '').startswith('Development/') else False,
    'SECRET_KEY': 'Some big sentence',
}

# Fix for https://bugs.chromium.org/p/chromium/issues/detail?id=162590
# In DEV we can use create_logout_url in Prod we'll define the logout url
if config['DEBUG']:
    LOGOUT_URL = users.create_logout_url('/')
else:
    LOGOUT_URL = '/_ah/logout?continue=https://' + gethostname() + '/'

API_KEY = 'secret_api_key'
