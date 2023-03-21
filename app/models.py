from . import db
from flask_login import UserMixin

#Defining "Models" (Tables)
class Role(db.Model): 
    __tablename__ = 'Role' 
    RoleID = db.Column(db.Integer, primary_key=True, nullable=False) 
    RoleName = db.Column(db.String(64), unique=True, nullable=False) 

    Users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self): 
        return '<Role %r>' % self.RoleName 
        
class User(db.Model, UserMixin): 
    __tablename__ = 'User' 
    UserID = db.Column(db.Integer, primary_key=True, nullable=False) 
    Username = db.Column(db.String(125), unique=True, index=True, nullable=False) 
    Password = db.Column(db.String(125), nullable=False) 
    Email = db.Column(db.String(255), unique=True, index=True, nullable=False) 
    RoleID = db.Column(db.Integer, db.ForeignKey('Role.RoleID'), nullable=False)
    
    User_Requests = db.relationship('UserRequest', backref='user', lazy=True)
    
    def __repr__(self): 
       return '<User %r>' % self.Username
    
class SoftwareRequest(db.Model):
    __tablename__ = 'SoftwareRequest' 
    RequestID = db.Column(db.Integer, primary_key=True)
    RequestTitle = db.Column(db.String(64), nullable=False) #Strayed a little off the model in a few areas...
    RequestDetails = db.Column(db.String(255), nullable=False)
    RequestImpact = db.Column(db.String(255), nullable=True)
    RequestDeadline = db.Column(db.DateTime, nullable=True)
    RequestImportance = db.Column(db.Integer, nullable=False)
    RequestAccepted = db.Column(db.Boolean, nullable=True)

    user_request = db.relationship('UserRequest', backref='software_request', uselist=False)

    def __repr__(self): 
       return '<SoftwareRequest %r>' % self.RequestTitle
    
class UserRequest(db.Model):
    __tablename__ = 'UserRequest' 
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID') ,primary_key=True, nullable=False)
    RequestId = db.Column(db.Integer, db.ForeignKey('SoftwareRequest.RequestID'),primary_key=True, nullable=False)
