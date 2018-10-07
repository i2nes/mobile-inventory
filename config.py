# Flask App Configurations
import os
from socket import gethostname
from google.appengine.api import users


config = {
    'DEBUG': True if os.getenv('SERVER_SOFTWARE', '').startswith('Development/') else False,
    'SECRET_KEY': 'Some big sentence',
}

API_KEY = 'secret_api_key'
