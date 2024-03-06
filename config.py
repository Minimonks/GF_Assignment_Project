from dotenv import load_dotenv
import os

class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.getenv('APP_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HTTPS_ONLY= os.getenv('HTTPS_ONLY')
    HSTS_MAX_AGE = 31536000
    
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