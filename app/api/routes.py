import logging
from . import app
from flask import Flask, jsonify, json, request
from google.appengine.api import users
from ..models import User, Device, DeviceTransaction
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


@app.route('/devices/info', methods=['GET'])
@api_key_required
def devices_status_api():

    if 'X-Api-Device-Id' in request.headers.keys():
        device = Device.get_by_id(str(request.headers['X-Api-Device-Id'].lower()))
        if device is not None:
            return jsonify(device.to_dict())
        else:
            return '', 404
    
    return '', 400


@app.route('/devices/alocate', methods=['POST'])
@api_key_required
def devices_alocate_api():

    if 'X-Api-Device-Id' in request.headers.keys() and 'X-Api-User-Id' in request.headers.keys():
        user = User.get_by_id(str(request.headers['X-Api-User-Id']).lower())
        device = Device.get_by_id(str(request.headers['X-Api-Device-Id']).lower())

        if user is None:
            errors = {
                'status': 404,
                'message': "User doesn't exist"
            }
            return jsonify(errors), 404

        if device is None:
            errors = {
                'status': 410,
                'message': "Device doesn't exist"
            }
            return jsonify(errors), 410

        if user is not None and device is not None:
            device.availability = False
            device.user_key = user.key
            transaction = DeviceTransaction()
            transaction.device_key = device.key
            transaction.user_key = user.key
            transaction.operation = 'checked out'

            # Update device info when it's included in the request body
            request_body = request.get_json()
            if request_body is not None:
                device.manufacturer = request_body['manufacturer'] if 'manufacturer' in request_body.keys() else device.manufacturer
                device.model = request_body['model'] if 'model' in request_body.keys() else device.model
                device.os = request_body['os'] if 'os' in request_body.keys() else device.os

            device.put()
            transaction.put()
        else:
            logging.info("Unexpected error alocating device")

    else:
        logging.info("Missing parameters")
        logging.info(request.headers.keys())
        errors = {
            'status': 400,
            'message': 'Unexpected or missing parameters'
        }
        return jsonify({}), 400

    return jsonify(device.to_dict()), 200


@app.route('/devices/register', methods=['POST'])
@api_key_required
def devices_register_api():

    if 'X-Api-Device-Id' in request.headers.keys():
        device = Device.get_by_id(str(request.headers['X-Api-Device-Id']).lower())
        if device is None:
            request_body = request.get_json()
            if request_body is not None:
                device = Device(id=str(request.headers['X-Api-Device-Id']).lower())
                device.manufacturer = request_body['manufacturer'] if 'manufacturer' in request_body.keys() else None
                device.model = request_body['model'] if 'model' in request_body.keys() else None
                device.os = request_body['os'] if 'os' in request_body.keys() else None
                transaction = DeviceTransaction()
                transaction.device_key = device.key
                transaction.operation = 'registered'

                device.put()
                transaction.put()
            else:
                logging.info("Unexpected or missing body while registering a device")
                logging.info(request_body)
                errors = {
                    'status': 400,
                    'message': 'Unexpected or missing parameters'
                }
                return jsonify(errors), 400
        else:
            logging.info("Trying to registor a device that already exists: {}".format(request.headers['X-Api-Device-Id']))
            return jsonify({}), 204
    else:
        logging.info("Missing header: X-Api-Device-Id")
        logging.info(request.headers.keys())

    return jsonify({}), 204


@app.route('/devices/free', methods=['POST'])
@api_key_required
def devices_free_api():

    if 'X-Api-Device-Id' in request.headers.keys() and 'X-Api-User-Id' in request.headers.keys():
        user = User.get_by_id(str(request.headers['X-Api-User-Id']).lower())
        device = Device.get_by_id(str(request.headers['X-Api-Device-Id']).lower())
        if user is not None and device is not None:
            device.user_key = None
            device.availability = True
            transaction = DeviceTransaction()
            transaction.device_key = device.key
            transaction.user_key = user.key
            transaction.operation = 'checked in'

            device.put()
            transaction.put()

        else:
            logging.info("Unexpected user or device")
            logging.info(request.headers['X-Api-User-Id'])
            logging.info(request.headers['X-Api-Device-Id'])
    else:
        logging.info("Missing parameters")
        logging.info(request.headers.keys())

    return jsonify(device.to_dict())