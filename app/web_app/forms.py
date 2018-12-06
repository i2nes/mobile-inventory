from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators


class LoginForm(FlaskForm):

    email = StringField('email', [validators.Email()])
    password = PasswordField('password', [validators.DataRequired()])


class CreateUserForm(FlaskForm):

    email = StringField('email', [validators.Email()])
    name = StringField('name', [validators.DataRequired()])
    password = PasswordField('Password', [validators.InputRequired(), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Repeat Password')


class ResetPasswordLinkForm(FlaskForm):

    email = StringField('email', [validators.Email()])


class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password', [validators.InputRequired(), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Repeat Password')


class EditDeviceForm(FlaskForm):

    manufacturer = StringField('Manufacturer', [validators.DataRequired()])
    model = StringField('Model', [validators.DataRequired()])
    lockModel = BooleanField()


class EditUserForm(FlaskForm):

    name = StringField('name', [validators.DataRequired()])
    isAdmin = BooleanField()
