from flask import Blueprint, flash, render_template,session,url_for,redirect
from .. import db
from ..models import User, SoftwareRequest, UserRequest
from.forms import LoginForm, RequestAccountForm, RequestSoftwareForm
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main',__name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Username=form.username.data).first()
        if user:
            if check_password_hash(user.Password ,form.password.data):
                login_user(user)
                flash("Logged in.")
                return redirect(url_for('main.home'))
            else:
                flash("Wrong Password!")
        else:
            flash("No user found...")

    #GET
    if current_user.is_authenticated:    
     return redirect(url_for('main.home'))
    else:
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

        hashed_pw = generate_password_hash(form.password.data, "sha256")
        
        user = User(Username = form.username.data, Email = form.email.data, Password = hashed_pw, RoleID = roleId)
        db.session.add(user)
        db.session.commit()
        flash("Account Created")
        return redirect(url_for('main.login'))
    
    if current_user.is_authenticated:    
     return redirect(url_for('main.home'))
    else:
     return render_template("requestAccount.html",form=form)

@main.route("/CreateRequest", methods=['GET', 'POST'])
@login_required
def createRequest():

    form = RequestSoftwareForm()

    if form.validate_on_submit():
       softwareReq = SoftwareRequest(RequestTitle = form.title.data, RequestDetails = form.details.data, RequestImpact = form.impact.data, RequestDeadline = form.deadline.data, RequestImportance = form.importance.data )
       db.session.add(softwareReq)

       reqId = db.session.query(db.func.max(SoftwareRequest.RequestID)).scalar()

       userReq = UserRequest(UserID=current_user.id, RequestId = reqId) 
       db.session.add(userReq)

       db.session.commit()
       flash("Request Created")
       return redirect(url_for('main.home'))

    return render_template("createRequest.html", form=form)