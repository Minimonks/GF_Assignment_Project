from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo #, Email


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:',  validators=[DataRequired()])
    submit = SubmitField('Submit')

class RequestAccountForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()]) #, Email()
    password = PasswordField('Password:',  validators=[DataRequired(), EqualTo('confirmPassword', message='Passwords must match')])
    confirmPassword = PasswordField('Confirm Password:', validators=[DataRequired()])
    role = BooleanField('Admin Account') #May be more roles in future ofc... but now... only admin/user
    submit = SubmitField('Request Account')