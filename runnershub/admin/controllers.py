from flask import Blueprint, request, current_app
from flask_security.decorators import roles_required
from runnershub.data.models import *
from sqlalchemy import exc
import json

admin = Blueprint('admin', __name__)

@admin.route('/user', methods=['GET'])
@roles_required('Admin')
def get_users():
	data = {}

	for user in User.query.all():
		data[user.email] = {'roles':user.roles}

	return Response(json.dumps(data), status=200, mimetype='application/json')

@admin.route('/user/create', methods=['POST'])
@roles_required('Admin')
def create_user():
	user_request = request.get_json()
	ret, status = {'response':'User created!'}, 201

	try:
		current_app.logger.debug("Creating user with email %s" % user_request['email'])

		newuser = User(user_request['email'], user_request['password'], user_request['roles'])
		db.session.add(newuser)
		db.session.commit()
		ret['id'] = newuser.id

	except KeyError as e:
		ret['response'] = "User creation failed!"
		ret['error'] = "Required key not provided: %s" % e
		status = 400

	except exc.SQLAlchemyError as e:
		ret['response'] = "User creation failed!"
		ret['error'] = e
		status = 500
	
	return Response(json.dumps(ret), status=status, mimetype='application/json')
