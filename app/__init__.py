import logging
from flask import Flask


def create_app(config):

    logging.info("STARTUP: Getting ready to launch")

    app = Flask(__name__)
    app.config.update(config)

    logging.info("STARTUP: Register Flask Blueprints")
    
    from .web_app import app as web_app_blueprint
    app.register_blueprint(web_app_blueprint, url_prefix='/')

    from .api import app as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    logging.info('STARTUP: READY TO ROCK!!!')

    return app



