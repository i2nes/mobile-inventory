from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class LoginForm(FlaskForm):

    email = StringField('email', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])