import os

from flask import Flask, session
from config import Config
from datetime import timedelta
from flask_login import LoginManager
from flask_session import Session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# intialize Flask app and specify view for login form to 
# override default 401 error
app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
  raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem and to timeout after x minutes
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config.from_object(Config)
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db.query_property()
import models 
Base.metadata.create_all(bind=engine)

# Auto remove database sessions when app shuts down
@app.teardown_appcontext
def shutdown_session(exception=None):
  db.remove()

import routes
