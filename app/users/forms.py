from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    username=StringField('Username', 
                        validators=[DataRequired(), Length(min=2,max=20)])

    email=StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', 
                                validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', 
                                        validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):   
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("That username is taken, Please choose a different one")
   
    def validate_email(self, email):
        user = User.query.filter(User.email.ilike(email.data)).first()
        if user:
            raise ValidationError("Account for this email exists, If you have already registerd, please try to login or reset password") 

class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', 
                                validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class ResetRequestForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter(User.email.ilike(email.data)).first()
        if user is None:
            raise ValidationError("There is no Account for this email. You must register first")
             
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
                                validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', 
                                        validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Reset Password')

class UpdateAccountForm(FlaskForm):
    username=StringField('Username', 
                        validators=[DataRequired(), Length(min=2,max=20)])

    email=StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picure', validators =[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError(current_user.username + " != " + username.data + ", That username is taken, Please choose a different one")
   
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter(User.email.ilike(email.data)).first()
            if user:
                raise ValidationError(current_user.email + " !=" + email.data + ", email exists, If you have already registerd, please try to login or reset password") 


