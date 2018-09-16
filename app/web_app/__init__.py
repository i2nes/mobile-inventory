from flask import Blueprint

app = Blueprint('web_app', __name__)

from . import routes