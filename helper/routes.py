from flask import render_template, url_for, flash, redirect, request
from helper import app, db, bcrypt
from helper.forms import RegistrationForm, LoginForm, UpdateAccountForm
from helper.models import User
from flask_login import login_user, current_user, logout_user, login_required

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

@app.route("/")
def home():
  return render_template('index.html')

@app.route("/ammo")
def ammo():
    return render_template('ammo.html', ammoTypes=ammoTypes, title='Ammo')

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

    flash(f'Your account has been created, you are now able to login.', 'success')

    return redirect(url_for('login'))

  return render_template('register.html', title="Register",form=form)

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
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash("Login unsuccessful. Please check username and password.", 'danger')

  return render_template('login.html', title="Login",form=form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
  form = UpdateAccountForm()
  image_file = url_for('static', filename='images/'+'banners/'+'/skier-banner.jpg')
  return render_template("account.html", title='Account', image_file=image_file, form=form)