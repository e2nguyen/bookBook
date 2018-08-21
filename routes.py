from flask import flash, render_template, redirect, request, url_for 
from application import app, db
from flask_login import login_user, logout_user, current_user, login_required
from forms import * 
from models import *

@app.route('/')
@app.route('/index')
def index():
  user = {'username': 'Erica'}
  return render_template('index.html', title='Home', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index')) 
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.add(user)
    db.commit()
    flash("Congratulations, you're in {}!".format(user.username))
    return redirect(url_for('index')) 
    
@app.route('/login', methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index')) 
  form = LoginForm()
  if form.validate_on_submit():
    # Check if user is in the database
    user = User.query.filter_by(username=form.username.data).first()
    # If user doesn't exist or doesn't match password, error
    if user is None or not user.check_password(form.password.data) :
      flash('Incorrect username or password.')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    return redirect(url_for('index'))
  return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))      

#TESTING: remove later
@app.route('/book/<id>')
@login_required
def book(id):
    book = Book.query.get(int(id)) #change to get() later
    if not book:
      flash('No book!')
    reviews = [
        {'body': 'Test post #1'},
        {'body': 'Test post #2'}
    ]
    return render_template('book.html', book=book, reviews=reviews)