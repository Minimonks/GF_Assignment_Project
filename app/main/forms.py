#Forms here used to generate html forms within views.

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Optional, NumberRange, regexp
from flask import escape
import re


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:',  validators=[DataRequired()])
    submit = SubmitField('Login')

    def sanitise(self):
      self.username.data = escape(self.username.data)

class RequestAccountForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()]) #, Email()
    password = PasswordField('Password:',  validators=[DataRequired(), EqualTo('confirmPassword', message='Passwords must match'), Length(min=8, message="Password must be at least 8 characters long."), regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', message="Password must contain at least one uppercase letter, one lowercase letter, one number and one special character.")])
    confirmPassword = PasswordField('Confirm Password:', validators=[DataRequired()])
    role = BooleanField('Admin Account') #May be more roles in future ofc... but now... only admin/user
    submit = SubmitField('Request Account')

    def sanitise(self):
      self.username.data = escape(self.username.data)
      self.email.data = escape(self.email.data)

class RequestSoftwareForm(FlaskForm):
    title = StringField('Request Title:', validators=[DataRequired(), Length(max=64)])
    details = TextAreaField('Details:', validators=[DataRequired()])
    impact =  TextAreaField('Impact:')      
    deadline =  DateField('Due Date:', validators=[Optional()]) 
    importance = IntegerField('Importance', validators=[DataRequired(), NumberRange(min=0, max=5)]) 
    submit = SubmitField('Submit Request')
    
    def sanitise(self):
      self.title.data = escape(self.title.data)
      self.details.data = escape(self.details.data)
      self.impact.data = escape(self.impact.data)

class SoftwareDetailsForm(FlaskForm):
    title = StringField('Request Title:', validators=[DataRequired(), Length(max=64)])
    details = TextAreaField('Details:', validators=[DataRequired()])
    impact =  TextAreaField('Impact:')      
    deadline =  DateField('Due Date:', validators=[Optional()]) 
    importance = IntegerField('Importance', validators=[DataRequired(), NumberRange(min=0, max=5)]) 
    update = SubmitField('Update')
    delete = SubmitField('Delete')
    accept = SubmitField('Accept')
    reject = SubmitField('Reject')

    def sanitise(self):
        self.title.data = escape(self.title.data)
        self.details.data = escape(self.details.data)
        self.impact.data = escape(self.impact.data)

  