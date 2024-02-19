import os

class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = 'Georges_Secret_Key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#Development configuration, please adjust SQLALCHEMY_DATABASE_URI to your DB Details. Link below is an example connection to an SSMS DB with Windows authentication.
class Development(Config):
    DEBUG=True
    #SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://:@(LocalDB)\GeorgesLocalDB/GFAssignmentDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///GFSEDODB.db'

#Testing configuration, please adjust SQLALCHEMY_DATABASE_URI to your DB Details. Link below is an example connection to an SSMS DB with Windows authentication. DO NOT SET THE SAME AS DEV DB AS UNIT TESTS WILL DROP DATA.
class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://:@(LocalDB)\GeorgesLocalDB/GeorgeAssignmentTestDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'

config = {
    'development': Development,
    'testing': Testing,

    'default': Development
}