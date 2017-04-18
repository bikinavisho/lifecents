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


@socket_io.on('deletion')
def socket_message_deletion(chosen_id):
	selected_one = dataBaser.Budget.query.filter_by(id=chosen_id).first()
	db.session.delete(selected_one)
	db.session.commit()
	print('DB entry deleted')


@socket_io.on('request_data')
def socket_message(request):
	print("request received for data")
	if request == 'budget':
		budgets = dataBaser.Budget.query.filter_by(user_id=dataBaser.User.query.get(flask.session['auth_user']).id).all()
		# Separate them into income category and expense category
		incomes = []
		expenses = []
		for budget in budgets:
			if budget.type:
				expenses.append(budget)
			else:
				incomes.append(budget)

		expense_packet = []
		for exp in expenses:
			expense_packet.append({'name': exp.name, 'value': exp.value})

		income_packet = []
		for inc in incomes:
			income_packet.append({'name': inc.name, 'value': inc.value})

		print("packet sent")
		socket_io.emit('json', {'expenseArray': expense_packet, 'incomeArray': income_packet})
