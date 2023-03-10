from flask import Blueprint, render_template,session,url_for,redirect
from .. import db
from ..models import User



main = Blueprint('main',__name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route("/about/")
def about():
    return render_template("about.html")