#Main routes file for application. Managing url pathways and data to pass
#When learning how to update I made refrence to (Elder, How To Update A Record In The Database - Flask Fridays #10 2021)
#Flask Mitigation studies came from (Elder, How To Migrate Database With Flask - Flask Fridays #11 2021)
#User login and password hashing came from (Elder, User Login with Flask_Login - Flask Fridays #22 2021), (Elder, Create A User Dashboard - Flask Fridays #23 2021), (Flask-SQLAlchemy, Login) and (Elder, Hashing Passwords With Werkzeug - Flask Fridays #13 2021)

from flask import Blueprint, flash, render_template,session,url_for,redirect, request
from .. import db
from ..models import User, SoftwareRequest, UserRequest
from.forms import LoginForm, RequestAccountForm, RequestSoftwareForm, SoftwareDetailsForm
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import limiter

main = Blueprint('main',__name__)

@main.route('/', methods=['GET', 'POST'])
@main.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute", error_message="Too many requests, please try again later.")
def login():
    form = LoginForm()
    #If there is a POST request, check if user exists, if so, if their password hash matches.
    if form.validate_on_submit():
        form.sanitise()
        user = User.query.filter_by(Username=form.username.data).first()
        if user:
            if check_password_hash(user.Password ,form.password.data):
                login_user(user)
                flash("Logged in.", "warning")
                return redirect(url_for('main.home'))
            else:
                flash("Incorrect credentials!", 'danger')
        else:
            flash("Incorrect credentials", 'danger')

    #GET - If logged in, redirect to home...
    if current_user.is_authenticated:
     return redirect(url_for('main.home'))
    else:
     return render_template('login.html', form=form)


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Logged out.","warning")
    return redirect(url_for('main.login'))

@main.route("/home/")
@main.route("/home/<status>")
@login_required
def home(status=None): 
    #If the user is admin, show all requests releant to requested status. If user, only show their own requests.
    if current_user.RoleID ==  1: #User
        role="User"
        requests = (db.session.query(SoftwareRequest).join(UserRequest, SoftwareRequest.RequestID == UserRequest.RequestId).filter((UserRequest.UserID == current_user.id) & (SoftwareRequest.RequestAccepted == status)).all())
        return render_template('index.html', role=role, requests=requests, status=status)
    else: #Admin
     role="Admin"               
     requests = SoftwareRequest.query.filter_by(RequestAccepted=status).all()
     return render_template('index.html', role=role, requests=requests, status=status)


@main.route("/about/")
def about():
    return render_template("about.html")

@main.route("/RequestAccount/", methods=['GET', 'POST'])
def reqAccount():
    form = RequestAccountForm()
    #POST - creates user in DB with hashed password.
    if form.validate_on_submit():
        form.sanitise()
        roleId = 2 if form.role.data else 1

        hashed_pw = generate_password_hash(form.password.data, "sha256")
        
        user = User(Username = form.username.data, Email = form.email.data, Password = hashed_pw, RoleID = roleId)
        db.session.add(user)
        db.session.commit()
        flash("Account Created","success")
        return redirect(url_for('main.login'))
    
    #If user is logged in, they shouldn't be requesting account... redirect
    if current_user.is_authenticated:    
     return redirect(url_for('main.home'))
    else:
     return render_template("requestAccount.html",form=form)

@main.route("/CreateRequest", methods=['GET', 'POST'])
@login_required
def createRequest():
    
    form = RequestSoftwareForm()

    #If all form data has been validated i.e. required fields filled, create request
    if form.validate_on_submit():
       form.sanitise()
       softwareReq = SoftwareRequest(RequestTitle = form.title.data, RequestDetails = form.details.data, RequestImpact = form.impact.data, RequestDeadline = form.deadline.data, RequestImportance = form.importance.data )
       db.session.add(softwareReq)

       #getting new request ID for population of UserRequest (linking current user to new request)
       reqId = db.session.query(db.func.max(SoftwareRequest.RequestID)).scalar()

       userReq = UserRequest(UserID=current_user.id, RequestId = reqId) 
       db.session.add(userReq)

       db.session.commit()
       flash("Request Created","success")
       return redirect(url_for('main.home'))

    return render_template("createRequest.html", form=form)

@main.route("/RequestDetails/<int:requestID>", methods=['GET', 'POST'])
@login_required
def requestDetails(requestID):
 form = SoftwareDetailsForm()
 rq = db.session.query(SoftwareRequest).filter_by(RequestID = requestID).first()
 userRequest = db.session.query(UserRequest).filter_by(RequestId = requestID).scalar()
 requestUser = db.session.query(User).filter_by(id = userRequest.UserID).scalar()
 
 if request.method == "POST":
    #Identifying  on post, which button was clicked
    if form.accept.data:
       print('Accepted')
       rq.RequestAccepted = True
       db.session.commit()
       
       flash("Request Accepted. This should now be a backlog item.","success")
    elif form.reject.data:
         print('Rejected')
         rq.RequestAccepted = False
         db.session.commit()


         flash("Request Rejected.","success")
    elif form.update.data:
         print('Updated')
         form.sanitise()
         rq.RequestTitle = form.title.data
         rq.RequestDetails = form.details.data
         rq.RequestImpact = form.impact.data
         rq.RequestDeadline = form.deadline.data
         rq.RequestImportance = form.importance.data
         db.session.commit()


         flash("Request Updated.","success")
    else:
         print('Deleted')
         db.session.delete(rq)
         db.session.delete(userRequest)
         db.session.commit()

         flash("Request Deleted.","success")    
  
    return redirect(url_for('main.home'))
 else:
    #  print('Normal load')
     
     #If the current user is NOT an admin, and tried to access a request other than their own... redirect.
     if current_user.RoleID == 1:
        if userRequest.UserID != current_user.id:
         return redirect(url_for('main.home'))
    

     form.title.data = rq.RequestTitle
     form.details.data = rq.RequestDetails
     form.impact.data = rq.RequestImpact
     form.deadline.data = rq.RequestDeadline
     form.importance.data = rq.RequestImportance

     disabledFields = False
     #If the request has been rejected/accepted, the user cannot update it. Also if the user did not make the request, they cannot update it. (Disables Fields)
     if rq.RequestAccepted is not None or userRequest.UserID != current_user.id:
       disabledFields = True

    #  print(disabledFields)
     return render_template("requestDetails.html", rq=rq, form=form, requestUser=requestUser, disabledFields=disabledFields)
 

