from flask import render_template, url_for, flash, redirect, request
from helper import app, db, bcrypt, mail
from helper.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from helper.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

ammoTypes = [
  {
    'type':'762x39',
    'rounds':
      [
        {
          'round_name':'HP',
          'damage':87,
          'penetration':15
        },
        {
          'round_name':'US',
          'damage':56,
          'penetration':29
        }
      ]
  },
  {
    'type':'762x51',
    'rounds':
      [
        {
          'round_name':'M61',
          'damage':99,
          'penetration':98
        },
        {
          'round_name':'M62',
          'damage':89,
          'penetration':88
        }
      ]
  },
]

##### HOME ROUTE #####
@app.route("/")
def home():
  return render_template('index.html')

##### AMMO ROUTE #####
@app.route("/ammo")
def ammo():
    return render_template('ammo.html', ammoTypes=ammoTypes, title='Ammo')

##### REGISTER ROUTE #####
@app.route("/register", methods=['GET', 'POST'])
def register():

  if current_user.is_authenticated:
    return redirect(url_for('home'))

  form = RegistrationForm()

  if form.validate_on_submit():

    # if form is valid hash the password
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

    # create a new user w/ the data input from the form and hashed password
    user = User(username= form.username.data, email= form.email.data, password= hashed_password) 

    # add the new user to the database
    db.session.add(user)
    db.session.commit()

    flash('Your account has been created, you are now able to login.', 'success')

    return redirect(url_for('login'))

  return render_template('register.html', title="Register",form=form)

##### LOGIN ROUTE #####
@app.route("/login", methods=['GET','POST'])
def login():

  if current_user.is_authenticated:
    return redirect(url_for('home'))

  form = LoginForm()

  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next') # next returns the page the user was trying to access before being redirected to the login page
      flash('You are now logged in.', "success")
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash("Login unsuccessful. Please check username and password.", 'danger')

  return render_template('login.html', title="Login",form=form)

##### LOGOUT ROUTE #####
@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))

##### ACCOUNT ROUTE #####
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()

  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated', "success")
    return redirect(url_for('account'))

  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email

  image_file = url_for('static', filename='images/'+'banners/'+'/skier-banner.jpg')
  return render_template("account.html", title='Account', image_file=image_file, form=form)

def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message('Password Reset Request', sender="tarkovtutor@gmail.com",recipients=[user.email])
  msg.body = f'''To reset your password visit the following link:
{url_for('reset_token',token=token,_external=True)}

If you did not make this request please ignore this email, no changes will be made to your account.'''
  mail.send(msg)

##### RESET PASSWORD ROUTE #####
@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('home'))

  form = RequestResetForm()

  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    send_reset_email(user)
    flash('An email has been sent with instructions to reset your password.', 'info')
    return redirect(url_for('login'))

  return render_template('reset_request.html', title='Reset Password', form=form)

##### CHANGE PASSWORD ROUTE #####
@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
  if current_user.is_authenticated:
    return redirect(url_for('home'))

  user = User.verify_reset_token(token)

  if user is None:
    flash('That token is invalid or expired.', 'warning')
    return redirect(url_for('login'))
  
  form = ResetPasswordForm()

  if form.validate_on_submit():
    # if form is valid hash the password
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    # add the new user to the database
    user.password = hashed_password
    db.session.commit()
    flash('Your password has been updated, you are now able to login.', 'success')
    return redirect(url_for('login'))

  return render_template('reset_token.html', title='Reset Password', form=form)