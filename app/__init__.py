# REFERENCES SECTION
'''
Create A User Dashboard - Flask Fridays #23 (2021) YouTube. Codemy. Available at: https://youtu.be/o0r_4zxz9z8 (Accessed: March 21, 2023). 

Declaring models (no date) Flask. Flask-SQLAlchemy. Available at: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/ (Accessed: March 18, 2023). 

Getting Started With Python Flask Blueprint | How to Structure And Configure Big Flask Project | HD (2020) YouTube. Available at: https://youtu.be/dITv8ZkH77A (Accessed: February 24, 2023). 

GRINBERG, M.I.G.U.E.L. (2018) “Chapters 1-7,” in Flask web development: Developing web applications with python. O'REILLY MEDIA, INC, USA, pp. 1–98. 

How To Update A Record In The Database - Flask Fridays #10 (2021) YouTube. Available at: https://www.youtube.com/watch?v=Wicjkn5_nIQ&amp;t=507s&amp;ab_channel=Codemy.com (Accessed: March 29, 2023). 

How To Migrate Database With Flask - Flask Fridays #11 (2021) YouTube. Codemy. Available at: https://youtu.be/ca-Vj6kwK7M (Accessed: March 24, 2023). 

Hashing Passwords With Werkzeug - Flask Fridays #13 (2021) YouTube. Codemy. Available at: https://youtu.be/8ebIEefhBpM (Accessed: March 21, 2023). 

Login (no date) Flask. Flask-SQLAlchemy. Available at: https://flask-login.readthedocs.io/en/latest/ (Accessed: March 10, 2023). 

User Login with Flask_Login - Flask Fridays #22 (2021) YouTube. Codemy. Available at: https://youtu.be/8ebIEefhBpM (Accessed: March 14, 2023). 

'''

#This is the initialising file for the application. App config is set to development, grabbing the development database connection string from config.py.
#To create the application structure and understand the basics of flask I had used both chapters 1-7 from (GRINBERG, 2018) and watched the video ( Abasimi, 2020)
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