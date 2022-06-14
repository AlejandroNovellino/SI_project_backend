from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class SignInForm(FlaskForm):
  email = StringField('email', validators=[DataRequired()])
  password = StringField('password', validators=[DataRequired()])
  username = StringField('username', validators=[DataRequired()])
  first_name = StringField('first_name', validators=[DataRequired()])
  last_name = StringField('last_name', validators=[DataRequired()])
  age = StringField('age', validators=[DataRequired()])
  nationality = StringField('nationality', validators=[DataRequired()])
  bio = StringField('bio', validators=[DataRequired()])
