from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import User

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
    'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Submit')
