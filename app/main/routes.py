from flask import Blueprint, render_template,session,url_for,redirect
from .. import db
from ..models import User
from.forms import LoginForm, RequestAccountForm

main = Blueprint('main',__name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # handle login logic
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)

@main.route("/home/")
def home():
    return render_template('index.html')

@main.route("/about/")
def about():
    return render_template("about.html")

@main.route('/', methods=['GET', 'POST'])
@main.route("/RequestAccount/")
def reqAccount():
    form = RequestAccountForm()
    return render_template("requestAccount.html",form=form)