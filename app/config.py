import os


class Config:
    SECRET_KEY = '@Key1621'
    SQLALCHEMY_DATABASE_URI = 'postgresql://kiama:kiamapwd@localhost/Flask-Blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}
