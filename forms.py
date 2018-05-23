from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignUpForm(Form):
    first_name = StringField('First name', validators=[DataRequired('Enter your first name')])
    last_name = StringField('Last name', validators=[DataRequired('Enter your last name')])
    email = StringField('Email', validators=[DataRequired('Enter your email'), Email('U done goofed, enter a valid email')])
    password = PasswordField('Password', validators=[DataRequired('Enter a password'), Length(min=6, message='Password must be 6 characters minimum') ])
    submit = SubmitField('Sign Up')

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired("Please Enter a email."), Email('Please enter ur email yo')])
    password = PasswordField('Password', validators=[DataRequired("Please enter a pwd yo")])
    submit = SubmitField("Sign In")