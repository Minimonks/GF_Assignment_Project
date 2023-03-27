from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(app_config = 'development'):
    app = Flask(__name__)
    app.config.from_object(config[app_config])

    bootstrap.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    from app.main.routes import main

    app.register_blueprint(main)

    return app