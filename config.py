import os

class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = 'Georges_Secret_Key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://:@(LocalDB)\GeorgesLocalDB/GFAssignmentDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'


class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://:@(LocalDB)\GeorgesLocalDB/GeorgeAssignmentTestDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'

config = {
    'development': Development,
    'testing': Testing,

    'default': Development
}