from flask import Blueprint, flash, render_template,session,url_for,redirect
from .. import db
from ..models import User
from.forms import LoginForm, RequestAccountForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

main = Blueprint('main',__name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.username.data).first()
        if user:
            if user.Password == form.password.data:
                login_user(user)
                flash("Logged in.")
                return redirect(url_for('main.home'))
            else:
                flash("Wrong Password!")
        else:
            flash("No user found...")
        
    return render_template('login.html', form=form)

@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for('main.login'))

@main.route("/home/")
@login_required
def home():
    return render_template('index.html')

@main.route("/about/")
def about():
    return render_template("about.html")

@main.route("/RequestAccount/", methods=['GET', 'POST'])
def reqAccount():
    form = RequestAccountForm()

    if form.validate_on_submit():
        roleId = 2 if form.role.data else 1
        user = User(Username = form.username.data, Email = form.email.data, Password = form.password.data, RoleID = roleId)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template("requestAccount.html",form=form)