import os


class Config:
    SECRET_KEY = '@Key1621'
    SQLALCHEMY_DATABASE_URI = 'postgresql://kiama:kiamapwd@localhost/Flask-Blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI = 'postgresql://ejkzdidlscvspo:6b00bc2c35912951c6340740ad71d3083808d257b133abc308e472aac9dcb557@ec2-3-209-61-239.compute-1.amazonaws.com:5432/dabln469vn7fbe'


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}
