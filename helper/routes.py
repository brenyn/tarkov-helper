from flask import render_template, url_for, flash, redirect, request
from helper import app, db, bcrypt, mail
from helper.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from helper.models import User, Ammo
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


##### HOME ROUTE #####
@app.route("/")
def home():
  return render_template('index.html')

##### AMMO ROUTE #####
ammoTypes= []
calibers=['12 Gauge Shot',
  '12 Gauge Slugs',
  '20 Gauge',
  '9x18mm',
  '7.62x25mm',
  '9x19mm',
  '0.45',
  '9x21mm',
  '5.7x28 mm',
  '4.6x30 mm',
  '9x39mm',
  '0.366',
  '5.45x39 mm',
  '5.56x45 mm',
  '7.62x51 mm',
  '7.62x54R',
  '12.7x55 mm',]

class Caliber:
  def __init__(self, caliber):
    self.caliber = caliber
    self.div_id = caliber.replace(' ', '-').replace('.','-').lower()
    self.rounds=[]

for caliber in calibers:
  # append dictionary to ammoTypes list w/ keys 'type': caliber, 'rounds':[]
  appendCaliber= Caliber(caliber)
  # query by caliber
  for ammo in Ammo.query.filter_by(ammo_type=caliber):
    # print(ammo.round)
    # append each round of caliber to list of dictionaries containing round name/stats
    appendCaliber.rounds.append(dict(round=ammo.round, damage=ammo.damage,penetration=ammo.penetration,armor_damage=ammo.armor_damage,frag_chance=ammo.frag_chance))
  ammoTypes.append(appendCaliber)
  
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