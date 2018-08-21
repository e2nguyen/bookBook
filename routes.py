from flask import flash, render_template, redirect, request, url_for, request 
from application import app, db
from flask_login import current_user, login_required, login_user, logout_user
from forms import * 
from models import *
from sqlalchemy import or_

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
  if current_user.is_authenticated:
    if request.method == 'POST':
      search_input = request.form.get("Search")
      book = Book.query.filter(or_(Book.isbn == search_input, Book.title == search_input,
                                   Book.author == search_input)).first()
      reviews = [
        {'body': 'Test post #1'},
        {'body': 'Test post #2'}
      ]
  
      if book: 
        return redirect(url_for('book', isbn=book.isbn))
      else:  
        flash("We couldn't find the book. Sorry about that. :<")
  
  return render_template('index.html', title='Home')


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
@login_required       # precautionary step; shouldn't be necessary though bc
def logout():
  logout_user()
  return redirect(url_for('index'))      

#TESTING: remove later
@app.route('/book/<isbn>', methods=['GET', 'POST', 'PUT'])
@login_required
def book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if not book:
      flash('No book!')
    reviews = [
        {'body': 'Test post #1'},
        {'body': 'Test post #2'}
    ]
    return render_template('book.html', book=book, reviews=reviews)
