import logging
from . import app
from google.appengine.ext import ndb
from flask import render_template, url_for, redirect, flash
from ..models import User, Device, DeviceTransaction, TemporaryUrl
from ..utils import reset_password_email, random_password
from forms import LoginForm, CreateUserForm, ResetPasswordLinkForm, ResetPasswordForm, EditDeviceForm
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
            return redirect(url_for('web_app.inventory_page'))
        elif len(User.query().fetch()) == 0:
            # Create first user from Sign in 
            user = User(id=form.email.data)
            user.password = generate_password_hash(form.password.data)
            user.put()
            logging.info("First sign in - Create user")
        else:
            logging.info("Login failed for {}".format(form.email.data))
            flash("Invalid login")
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

    if not current_user.is_admin():
        return render_template('not_found_page.html'), 404

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

    random_pass = random_password()

    return render_template(
        'create_user_page.html',
        nav_link='create_user_page',
        form=form,
        random_pass=random_pass)


@app.route('inventory/')
def inventory_page():
    devices_ndb = Device().query().fetch()
    return render_template(
        'inventory_page.html',
        nav_link='inventory_page',
        devices=devices_ndb,
        device_count=len(devices_ndb))


@app.route('users/<user_id>')
@login_required
def user_edit_page(user_id):
    return 'future user edit page'


@app.route('devices/<device_id>')
@login_required
def device_page(device_id):
    device = Device.get_by_id(str(device_id).lower())
    if device:
        device_history = DeviceTransaction().query(DeviceTransaction.device_key==device.key).order(-DeviceTransaction.transaction_date).fetch()
        return render_template(
            'device_page.html',
            device=device,
            device_history=device_history)
    else:
        return render_template('not_found_page.html'), 404


@app.route('logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web_app.home_page'))


@app.route('resetpassword/', methods=['GET', 'POST'])
def reset_password_page():

    if current_user.is_authenticated:
        return redirect(url_for('web_app.inventory_page'))
    
    form = ResetPasswordLinkForm()

    if form.validate_on_submit():

        reset_email = form.email.data
        user = User.get_by_id(reset_email)

        if user:
            reset_password_email(reset_email)
        else:
            logging.info('Reset password attempt with user: {}'.format(reset_email))

        return render_template('email_sent_page.html')

    return render_template('reset_password_page.html', form=form)


@app.route('resetpassword/<urlsafe_string>', methods=['GET', 'POST'])
def reset_password_link_page(urlsafe_string):

    try:
        temp_url = TemporaryUrl.get_by_id(int(urlsafe_string))
    except Exception as e:
        logging.info(e)
        return render_template('not_found_page.html'), 404

    if not temp_url.isActive():
        logging.info('password reset link expired')
        return render_template('not_found_page.html'), 404

    if not temp_url.user_key:
        logging.info('Reset link with no user key')
        return render_template('not_found_page.html'), 404

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = temp_url.user_key.get()
        user.password = generate_password_hash(form.password.data)
        user.put()
        temp_url.isValid = False
        temp_url.put()
        return redirect(url_for('web_app.home_page'))

    return render_template('reset_password_link_page.html', form=form, urlsafe_string=urlsafe_string)


@app.route('emailsent/')
def email_sent_page():
    return render_template('email_sent_page.html')


@app.route('devices/<device_id>/delete', methods=['POST'])
def delete_device_handler(device_id):

    if not current_user.is_admin():
        return render_template('not_found_page.html'), 404

    logging.info("Deleting device {}".format(device_id))

    try:
        # try getting device_id from the datastore
        device = Device.get_by_id(str(device_id).lower())
    except Exception as e:
        logging.info("Error retrieving entity for deletion: Device {}".format(device_id))
        logging.info(e)
        # return a 404 in case of failure
        return render_template('not_found_page.html'), 404

    # If device exists, delete any associated transactions
    ndb.delete_multi(DeviceTransaction().query(DeviceTransaction.device_key==device.key).fetch(keys_only=True))

    # and finally, delete the device
    device.key.delete()

    logging.info("Device deleted")

    # Back to inventory page
    return redirect(url_for('web_app.inventory_page'))


@app.route('devices/<device_id>/edit', methods=['GET', 'POST'])
def edit_device_page(device_id):

    if not current_user.is_admin():
        return render_template('not_found_page.html'), 404

    device = Device.get_by_id(str(device_id).lower())

    if not device:
        return render_template('not_found_page.html'), 404
    
    form = EditDeviceForm()
    checked_status = "checked" if device.lockModelName else ""

    if form.validate_on_submit():
        device.manufacturer = form.manufacturer.data
        device.model = form.model.data
        device.lockModelName = form.lockModel.data
        device.put()
        return redirect(url_for('web_app.inventory_page'))

    return render_template('edit_device_page.html', form=form, device=device, checked_status=checked_status)