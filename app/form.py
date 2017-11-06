from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, BooleanField


class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
