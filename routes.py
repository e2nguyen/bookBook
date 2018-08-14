from flask import flash, render_template, redirect, request, url_for 
from application import app, db
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/index')
def index():
  user = {'username': 'Erica'}
  return render_template('index.html', title='Home', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
  #if current_user.is_authenticated:
  #  return 
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data. email=form.username.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash("Congratulations, you're in!")
    return redirect(url_for('index')) ###### change url_for and below line
  return render_template('index.html', title='Register', user=user)
