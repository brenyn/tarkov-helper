from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from helper.models import User

##### REGISTRATION FORM #####
class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

  email = StringField('Email', validators=[Optional(), Email()])

  password = PasswordField('Password', validators=[DataRequired()])

  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('Username is already in use. Please choose another.')

  def validate_email(self, email):
    email = User.query.filter_by(email=email.data).first()
    if email and email!= '':
      raise ValidationError('Email is already in use. Please choose another.')

##### LOGIN FORM #####
class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

  password = PasswordField('Password', validators=[DataRequired()])

  remember = BooleanField('Remember me')

  submit = SubmitField('Login')

##### UPDATE ACCOUNT FORM #####
class UpdateAccountForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

  email = StringField('Email', validators=[Email(), Optional()])

  submit = SubmitField('Update')

  def validate_username(self, username):
    if username.data != current_user.username:
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('Username is already in use. Please choose another.')

  def validate_email(self, email):
    if email.data != current_user.email and email.data != '':
      email = User.query.filter_by(email=email.data).first()
      if email:
        raise ValidationError('Email is already in use. Please choose another.')

##### REQUEST RESET FORM #####
class RequestResetForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Request Password Reset')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is None or user == '':
      raise ValidationError('There is no account with that email. You must register first.')

##### RESET PASSWORD FORM #####
class ResetPasswordForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Reset Password')