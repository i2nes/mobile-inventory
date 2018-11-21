# Flask App Configurations
# This is an example config file. Create a config.py with your own secrets.
import os
from socket import gethostname


config = {
    'DEBUG': True if os.getenv('SERVER_SOFTWARE', '').startswith('Development/') else False,
    'SECRET_KEY': 'Some big sentence',
}

API_KEY = 'secret_api_key'

APP_NAME = 'my_app_name'

EMAIL_WHITELIST = ['gmail.com']