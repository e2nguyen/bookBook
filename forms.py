from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from models import User

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
    'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Submit')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username.')

  def validate_email(self, email):
    email = User.query.filter_by(email=email.data).first()
    if email is not None:
      raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Submit')

class ReviewForm(FlaskForm):
  rating = RadioField('My rating:', coerce=int, choices=[ (1,''), 
                                                      (2,''),
                                                      (3,''), 
                                                      (4,''),
                                                      (5,'')
                                                    ])
  body = TextAreaField('Review:', validators=[Length(min=0, max=500)])
  submit = SubmitField('Submit')

 
