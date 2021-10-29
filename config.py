import os

class Config(object):
    SECRET_KEY = '02chicholta'


class DevelopmentConfig(Config):
    DEBUG =True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False