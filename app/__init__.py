import logging
from flask import Flask, render_template
from flask_login import LoginManager
from models import User


# HTTP 404 Handler
def page_not_found(e):
  return render_template('not_found_page.html'), 404


def create_app(config):

    logging.info("STARTUP: Getting ready to launch")

    app = Flask(__name__)
    app.config.update(config)
    app.register_error_handler(404, page_not_found)

    logging.info("STARTUP: Flask app ready")

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'web_app.home_page'

    # This callback is used to reload the user object
    # from the user ID stored in the session
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    logging.info("STARTUP: Loggin Manager ready")
    
    from .web_app import app as web_app_blueprint
    app.register_blueprint(web_app_blueprint, url_prefix='/')

    from .api import app as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    logging.info("STARTUP: Flask Blueprints registered")

    logging.info('STARTUP: READY TO ROCK!!!')

    return app



