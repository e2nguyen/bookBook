import requests

from flask import flash, jsonify, make_response, render_template, redirect, request, url_for, request, Response 
from application import app, db
from flask_login import current_user, login_required, login_user, logout_user
from forms import * 
from models import *
from sqlalchemy import or_, and_, func
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
  if current_user.is_authenticated:
    if request.method == 'POST':
      search_input = request.form.get("Search")
      books = Book.query.filter(or_(
                      Book.isbn.ilike("%" + search_input + "%"),
                      Book.title.ilike("%" + search_input + "%"),
                      Book.author.ilike("%" + search_input + "%"))).all()
      if len(books) == 1: 
        # if the search_input is an exact match, go directly book page
        book = Book.query.filter(or_(
                      func.lower(Book.isbn) == func.lower(search_input),
                      func.lower(Book.title) == func.lower(search_input),
                      func.lower(Book.author) == func.lower(search_input))).first()
        if book: 
          return redirect(url_for('book', isbn=book.isbn))
        # if search_input is not exact match, show list of potential books
        else:
          return render_template('index.html', title='Home', books=books)
      # if no books were found, print error message
      elif len(books) == 0:  
        flash("We couldn't find {}. Sorry about that. :<".format(search_input))
      # if multiple books found, show list of potential books
      else:
        return render_template('index.html', title='Home', books=books)
  return render_template('index.html', title='Home', books=None)


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
  return render_template('register.html', title='Register', form=form)

    
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
@login_required       # pecautionary step; shouldn't be necessary though bc
def logout():
  logout_user()
  return redirect(url_for('index'))      

@app.route('/book/<isbn>', methods=['GET', 'POST']) 
@login_required
def book(isbn):
  book = Book.query.filter_by(isbn=isbn).first()
  if not book:
    flash('No book!')
    return redirect(url_for('index')) 

  form = ReviewForm()
  if form.validate_on_submit():
    # does this user have a review for this book already?
    existing_review = Review.query.filter(and_(Review.user_id == current_user.id,
                                               Review.book_id == book.id)).first()

    # if never been reviewed, add the new review
    if existing_review:
       flash("You already reviewed this book. Stop being a lil' bitch.")
    else:
      review = Review(rating=form.rating.data, body=form.body.data, 
                      user_id=current_user.id, book_id=book.id)
      db.add(review)
      db.commit()
      flash("Thank you for your review, Big Bitch!")
  
  # get avg rating from goodreads
  res = requests.get("https://www.goodreads.com/book/review_counts.json", 
                      params={"key": "wbYVNp1WvHbg0SdF1fCvoA", 
                      "isbns": isbn})
  # check if get request was successful
  if res.status_code != 200:
    raise Exception('ERROR: API request unsuccessful.')
  data = res.json()
  rating = data['books'][0]['average_rating']
  num_ratings = data['books'][0]['work_ratings_count']              
  return render_template('book.html', book=book, reviews=book.reviews[::-1],
                          form=form, rating=rating, num_ratings=num_ratings)


# method for api access
@app.route('/api/<isbn>')
@login_required
def access(isbn):
  book = Book.query.filter_by(isbn=isbn).first()
  if not book:
    return jsonify({"error": "invalid isbn"}), 404
    #flash('No book!')
    #return redirect(url_for('index'))

  # get summed ratings from bookBook
  ratings = [rev.rating for rev in Review.query.filter_by(book_id=book.id).all()]  
  bookavg = sum(ratings)
  # get avg rating from goodreads
  goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", 
                      params={"key": "wbYVNp1WvHbg0SdF1fCvoA", 
                      "isbns": isbn})

  # check if get request was successful
  if goodreads.status_code != 200:
    raise Exception('ERROR: API request unsuccessful.')

  data = goodreads.json()
  gr_rating = float(data['books'][0]['average_rating'])
  num_ratings = int(data['books'][0]['work_ratings_count'])              
  review_count = num_ratings + len(ratings)
  
  average_score = round((((gr_rating * num_ratings) + bookavg)/review_count), 2)
  return Response(json.dumps({
                "title":  book.title,
                "author": book.author,
                "year": book.year,
                "book": isbn,
                "review_count": review_count,
                "average_score": average_score
                }), mimetype='application/json')
