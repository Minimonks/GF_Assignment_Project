from flask import Blueprint, flash, render_template,session,url_for,redirect, request
from .. import db
from ..models import User, SoftwareRequest, UserRequest
from.forms import LoginForm, RequestAccountForm, RequestSoftwareForm, SoftwareDetailsForm
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
                flash("Logged in.", "warning")
                return redirect(url_for('main.home'))
            else:
                flash("Wrong Password!", 'danger')
        else:
            flash("No user found...", 'danger')

    #GET
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
    if current_user.RoleID == 1: #User
        role="User"
        requests = (db.session.query(SoftwareRequest).join(UserRequest, SoftwareRequest.RequestID == UserRequest.RequestId).filter((UserRequest.UserID == current_user.id) & (SoftwareRequest.RequestAccepted == status)).all())
        return render_template('index.html', role=role, requests=requests)
    else: #Admin
     role="Admin"               
     requests = SoftwareRequest.query.filter_by(RequestAccepted=status).all()
     return render_template('index.html', role=role, requests=requests)


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
        flash("Account Created","success")
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
     print('Normal load')
     
     if current_user.RoleID == 1:
        if userRequest.UserID != current_user.id:
         return redirect(url_for('main.home'))
    

     form.title.data = rq.RequestTitle
     form.details.data = rq.RequestDetails
     form.impact.data = rq.RequestImpact
     form.deadline.data = rq.RequestDeadline
     form.importance.data = rq.RequestImportance

     disabledFields = False

     if rq.RequestAccepted is not None:
       disabledFields = True


     return render_template("requestDetails.html", rq=rq, form=form, requestUser=requestUser, disabledFields=disabledFields)
 

