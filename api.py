# API handles JS and socket requests
# key word: REQUESTS

import flask
from flask_socketio import join_room, send, emit, leave_room

from init import app, db, socket_io
import dataBaser


def check_request():
    token = flask.session['csrf_token']
    if flask.request.form['_csrf_token'] != token:
        app.logger.warn('invalid CSRF token')
        flask.abort(400)
    if flask.session.get('auth_user') != flask.g.user.id:
        app.logger.warn('requesting user %s not logged in (%s)',
                        flask.g.user.id,
                        flask.session.get('auth_user'))
        flask.abort(403)


# Received json message from the client
@socket_io.on('json')
def socket_message(data):
    # in here, 'data' is a Python object parsed from JSON
    # 'msg': thisValue, 'type': type, 'db-id': dbId,'csrf': csrf

    print("message received")

    # get data from json
    new_value = data['msg']
    data_type = data['type']
    db_id = data['db-id']
    csrf_token = data['csrf']

    # Authenticate action
    # check_request()

    # Find object in database
    this_budget = dataBaser.Budget.query.filter_by(id=db_id).first()

    if data_type == "value":
        # Cast to float before putting into database
        t_new_value = 0.0 + float(new_value)
        if t_new_value == this_budget.value:
            data_changed = False
        else:
            data_changed = True
            this_budget.value = t_new_value
    else:
        if new_value == this_budget.name:
            data_changed = False
        else:
            data_changed = True
            this_budget.name = new_value

    if data_changed:
        # Save Database changes
        db.session.commit()
        print("DB changed")


# Received string message from the client
@socket_io.on('message')
def socket_message(msg):
    # in here, 'msg' is a string
    emit('message', msg)

