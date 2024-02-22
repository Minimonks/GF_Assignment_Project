from dotenv import load_dotenv
import os

class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class Development(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.getenv('DBDev')

class Testing(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.getenv('DBTest')


config = {
    'development': Development,
    'testing': Testing,

    'default': Development
}