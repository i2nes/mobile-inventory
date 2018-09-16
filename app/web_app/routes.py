import logging
from . import app
from google.appengine.api import users
from flask import render_template, url_for
from ..utils import login_required
from config import LOGOUT_URL
from ..models import User, Device


@app.route('/')
def home_page():
    login_url = users.create_login_url(url_for('web_app.inventory_page'))
    return render_template('home_page.html', login_url=login_url)


@app.route('users/')
@login_required
def users_page():
    users_ndb = User().query().fetch()
    return render_template(
        'users_page.html',
        logout_url=LOGOUT_URL,
        nav_link='users_page',
        users=users_ndb)


@app.route('inventory/')
@login_required
def inventory_page():
    devices_ndb = Device().query().fetch()
    return render_template(
        'inventory_page.html',
        logout_url=LOGOUT_URL,
        nav_link='inventory_page',
        devices=devices_ndb)


@app.route('users/<user_id>')
@login_required
def user_edit_page(user_id):
    return 'user edit page'


@app.route('devices/<device_id>')
@login_required
def device_edit_page(device_id):
    return 'device edit page'
