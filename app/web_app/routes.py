import logging
from . import app
from google.appengine.api import users
from flask import render_template, url_for, redirect
from ..models import User, Device
from forms import LoginForm, CreateUserForm
from werkzeug.security import generate_password_hash
from flask_login import login_required, login_user, logout_user, current_user


@app.route('/', methods=['GET', 'POST'])
def home_page():

    if current_user.is_authenticated:
        return redirect(url_for('web_app.inventory_page'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.get_by_id(form.email.data)
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('web_app.users_page'))
        else:
            logging.info("Login failed for {}".format(form.email.data))
            return redirect(url_for('web_app.home_page'))

    return render_template('home_page.html', form=form, )


@app.route('users/')
@login_required
def users_page():
    users_ndb = User().query().fetch()
    return render_template(
        'users_page.html',
        nav_link='users_page',
        users=users_ndb)


@app.route('users/create', methods=['GET', 'POST'])
@login_required
def create_user_page():

    form = CreateUserForm()

    if form.validate_on_submit():
        user_query = User.get_by_id(form.email.data)
        if user_query:
            logging.info("User already exists")
        else:
            user = User(id=form.email.data)
            user.name = form.name.data
            user.password = generate_password_hash(form.password.data)
            user.put()
            return redirect(url_for('web_app.users_page'))

    return render_template('create_user_page.html', form=form)


@app.route('inventory/')
def inventory_page():
    devices_ndb = Device().query().fetch()
    return render_template(
        'inventory_page.html',
        nav_link='inventory_page',
        devices=devices_ndb)


@app.route('users/<user_id>')
@login_required
def user_edit_page(user_id):
    user = User.get_by_id(int(user_id))
    return user.email


@app.route('devices/<device_id>')
@login_required
def device_edit_page(device_id):
    return 'device edit page'


@app.route('logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web_app.home_page'))