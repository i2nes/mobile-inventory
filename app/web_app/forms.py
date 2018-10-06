from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):

    email = StringField('email_', validators=[DataRequired()])
    password = PasswordField('password_', validators=[DataRequired()])