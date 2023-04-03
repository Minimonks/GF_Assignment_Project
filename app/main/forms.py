from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Optional, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:',  validators=[DataRequired()])
    submit = SubmitField('Login')

class RequestAccountForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()]) #, Email()
    password = PasswordField('Password:',  validators=[DataRequired(), EqualTo('confirmPassword', message='Passwords must match')])
    confirmPassword = PasswordField('Confirm Password:', validators=[DataRequired()])
    role = BooleanField('Admin Account') #May be more roles in future ofc... but now... only admin/user
    submit = SubmitField('Request Account')

class RequestSoftwareForm(FlaskForm):
    title = StringField('Request Title:', validators=[DataRequired(), Length(max=64)])
    details = TextAreaField('Details:', validators=[DataRequired()])
    impact =  TextAreaField('Impact:')      
    deadline =  DateField('Due Date:', validators=[Optional()]) 
    importance = IntegerField('Importance', validators=[DataRequired(), NumberRange(min=0, max=5)]) 
    submit = SubmitField('Submit Request')

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