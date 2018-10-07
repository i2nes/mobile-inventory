import logging
from flask import Flask
from flask_login import LoginManager
from models import User


def create_app(config):

    logging.info("STARTUP: Getting ready to launch")

    app = Flask(__name__)
    app.config.update(config)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'web_app.home_page'

    # This callback is used to reload the user object
    # from the user ID stored in the session
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    logging.info("STARTUP: Register Flask Blueprints")
    
    from .web_app import app as web_app_blueprint
    app.register_blueprint(web_app_blueprint, url_prefix='/')

    from .api import app as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    logging.info('STARTUP: READY TO ROCK!!!')

    return app



