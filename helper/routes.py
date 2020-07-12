from flask import render_template, url_for, flash, redirect
from helper import app, db, bcrypt
from helper.forms import RegistrationForm, LoginForm
from helper.models import User

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
  form = LoginForm()
  if form.validate_on_submit():
    if form.username.data == 'remyS' and form.password.data == 'password':
      flash('You have been logged in!', 'success')
      return redirect(url_for('home'))
    else:
      flash("Login unsuccessful. Please check username and password.", 'danger')

  return render_template('login.html', title="Login",form=form)