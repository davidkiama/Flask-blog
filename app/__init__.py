from flask import Flask


from .config import config_options


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_options[config_name])

    # blueprint for auth parts of the app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of the app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
