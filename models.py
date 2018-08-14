from application import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String

class User(UserMixin):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(32), index=True, unique=True)
  email = Column(String(64), index=True, unique=True)
  password_hash = Column(String(128))
  
  def __repr__(self):
    return '<User {}, email {}>'.format(self.username, self.email)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

#@login.user_loader
#def load_user(id):
#  return User.query.get(int(id))
