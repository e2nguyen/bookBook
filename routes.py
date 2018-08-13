from flask import render_template, url_for, request
from application import app
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def index():
  user = {'username': 'Erica'}
  return render_template('index.html', title='Home', user=user)
