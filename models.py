from application import Base, login 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base, UserMixin):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(32), index=True, unique=True)
  email = Column(String(64), index=True, unique=True)
  password_hash = Column(String(128))
  reviews = relationship('Review', backref='user', lazy='dynamic')

  '''
  def __init__(self, username=None, email=None):
    self.username = username
    self.email = email
  '''
  def __repr__(self):
    return '<user: {}, email: {}>'.format(self.username, self.email)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class Book(Base):
  __tablename__ = 'books2'
  id = Column(Integer, primary_key=True)
  isbn = Column(String(20))
  title = Column(String(100))
  author = Column(String(100))
  year = Column(String(4))
  reviews = relationship('Review', backref='books2', lazy='dynamic')

  def __repr__(self):
    return '<title: {}, author: {}>'.format(self.title, self.author)

class Review(Base):
  __tablename__='reviews'
  id = Column(Integer, primary_key=True)
  rating = Column(String(10))
  body = Column(String(500))
  user_id = Column(Integer, ForeignKey('users.id'))
  book_id = Column(Integer, ForeignKey('books2.id'))