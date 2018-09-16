import logging
from . import app
from flask import Flask, jsonify, json, request
from google.appengine.api import users
from ..models import User, Device
from ..utils import api_key_required


@app.route('/users', methods=['GET'])
@api_key_required
def users_api():
    users_ndb = User.query().fetch()
    return jsonify({'users': [u.to_dict() for u in users_ndb] }), 200


@app.route('/devices', methods=['GET'])
@api_key_required
def devices_api():
    devices_ndb = Device.query().fetch()
    return jsonify({'Devices': [d.to_dict() for d in devices_ndb] }), 200


@app.route('/devices/alocate', methods=['POST'])
@api_key_required
def devices_alocate_api():

    if 'X-Device-Id' in request.headers.keys() and 'X-User-Id' in request.headers.keys():
        user = User.get_by_id(int(request.headers['X-User-Id']))
        device = Device.get_by_id(request.headers['X-Device-Id'])
        if user is not None:
            if device is None:
                device = Device(id=request.headers['X-Device-Id'])
            device.user_key = user.key
            device.put()
    else:
        logging.info("Missing parameters")
        logging.info(request.headers.keys())

    return '', 204


@app.route('/devices/free', methods=['POST'])
@api_key_required
def devices_free_api():

    if 'X-Device-Id' in request.headers.keys() and 'X-User-Id' in request.headers.keys():
        user = User.get_by_id(int(request.headers['X-User-Id']))
        device = Device.get_by_id(request.headers['X-Device-Id'])
        if user is not None and device is not None:
            device.user_key = None
            device.put()
        else:
            logging.info("Unexpected user or device")
    else:
        logging.info("Missing parameters")
        logging.info(request.headers.keys())

    return '', 204