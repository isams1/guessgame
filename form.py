from flask_wtf import Form
from wtforms import TextField, PasswordField, validators
from wtforms.validators import *

class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password', [validators.Required(),
    	validators.EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Confirm Password')