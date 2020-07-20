from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Required, Length, EqualTo, Email
from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField('Enter your email', validators=[Required(), Email()])
    username = StringField('Username', validators=[Required(), Length(min=6, max=20, message="Username should be more than 6 characters")])
    password = PasswordField('Enter password', validators=[Required(), EqualTo('confirm_password', message='Passwords should match'), Length(min=6, max=20, message="Password should be between 6 and 20 characters")])
    bio = TextAreaField('About yourself')    
    confirm_password = PasswordField('Repeat password', validators=[Required()])
    submit = SubmitField('Sign Up')

     
    def validate_username(self, data_field):
        if User.query.filter_by(name=data_field.data).first():
            raise ValidationError('Username is taken')

    def validate_email(self, data_field):
        if User.query.filter_by(email=data_field.data).first():
            raise ValidationError('Email is taken')

class LoginForm(FlaskForm):
    email = StringField('Enter your email', validators=[Required(), Email()])
    password = PasswordField('Your password', validators=[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')

