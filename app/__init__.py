from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(app_config = 'development'):
    app = Flask(__name__)
    app.config.from_object(config[app_config])

    bootstrap.init_app(app)
    db.init_app(app)
    
    from app.main.routes import main

    app.register_blueprint(main)

    return app