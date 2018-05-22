from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class SignUpForm(Form):
    first_name = StringField('First name', validators=[DataRequired('Enter your first name')])
    last_name = StringField('Last name', validators=[DataRequired('Enter your last name')])
    email = StringField('Email', validators=[DataRequired('Enter your email')])
    password = PasswordField('Password', validators=[DataRequired('Enter a password')])
    submit = SubmitField('Sign Up')