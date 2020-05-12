import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def user_index():
	users = models.User.select()
	user_dicts = [model_to_dict(user) for user in users]

	# remove password
	for user_dict in user_dicts:
		user_dict.pop('password')

		print(user_dicts)

		# response
		return jsonify(
			user_dicts
		), 200

### REGISTER ROUTE -- POST ###
@users.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	payload['name'] = payload['name']
	payload['city'] = payload['city']
	payload['state'] = payload['state']
	payload['country'] = payload['country']
	payload['email'] = payload['email'].lower()
	payload['shelter'] = payload['shelter']
	print(payload)

	# logic to see if user exists
	try:
		models.User.get(models.User.email == payload['email'])

		return jsonify(
			data={},
			message=f"An account with the email {payload['email']} already exists",
			status=401
		), 401
	# if they do not
	except models.DoesNotExist:
		# scramble password with bcrypt
		pw_hash = generate_password_hash(payload['password'])

		# create user
		create_user = models.User.create(
			name=payload['name'],
			city=payload['city'],
			state=payload['state'],
			country=payload['country'],
			email=payload['email'],
			password=pw_hash,
			shelter=payload['shelter']
		)
		print(create_user)

		# logs in user and starts session
		login_user(create_user)

		create_user_dict = model_to_dict(create_user)
		print(create_user_dict)

		create_user_dict.pop('password')

		# response
		return jsonify(
			data=create_user_dict,
			message=f"Successfully registered account for {create_user_dict['name']} with email {create_user_dict['email']}",
			status=201
		), 201


### LOGIN ROUTE -- POST ###
@users.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	payload['name'] = payload['name']
	payload['city'] = payload['city']
	payload['state'] = payload['state']
	payload['country'] = payload['country']
	payload['email'] = payload['email']
	payload['shelter'] = payload['shelter']

	# logic to look up user by email
	try:
		user = models.User.get(models.User.email == payload['email'])
		user_dict = model_to_dict(user)

		# user exists, check password
		# 1st arg -- the encrypted password you are checking against
		# 2nd arg -- the password attempt you are trying to verify
		password_is_good = check_password_hash(user_dict['password'], payload['password'])

		# logic if password is valid
		if(password_is_good):
			login_user(user)

			# remove password
			user_dict.pop('password')

			# response
			return jsonify(
				data=user_dict,
				message=f"{user_dict['name']} successfully logged in!",
				status=200
			), 200
		# logic if password is invalid
		else:
			print('password is no good')

			# response
			return jsonify(
				data={},
				message="Email or password is invalid",
				status=401
			), 401
	# logic if user does not exist
	except models.DoesNotExist:
		print('username is invalid')

		# response
		return jsonify(
			data={},
			message="Email or password is invalid",
			status=401
		), 401


### START OF TEMPORARY ROUTE ###
@users.route('/logged_in_user', methods=['GET'])
def currently_logged():
	print(current_user)
	print('is current_user a shelter')
	print(current_user.shelter)
	# current_user.is_authenticated allows you to see whether a user is logged in
	if not current_user.is_authenticated:

		# response
		return jsonify(
			data={},
			message="No user is currently logged in",
			status=401
		), 401
	# access to currently logged user
	else:
		user_dict = model_to_dict(current_user)
		user_dict.pop('password')

		# response
		return jsonify(
			data=user_dict,
			message=f"Currently logged in as user {user_dict['name']} with email {user_dict['email']}",
			status=200
		), 200
### END OF TEMPORARY ROUTE ###


### USER SHOW ROUTE -- GET ###
@users.route('/<id>', methods=['GET'])
def show_user(id):
	user = models.User.get(models.User.id == id)
	user_dict = model_to_dict(user)
	user_dict.pop('password')
	print(user_dict)
	return jsonify(
		data=user_dict,
		message=f"Here is information about {user_dict['name']}",
		status=200
	), 200


### LOGOUT ROUTE -- GET ###
@users.route('/logout', methods=['GET'])
def logout():
	
	logout_user()

	# response
	return jsonify(
		data={},
		message="Successfully logged out!",
		status=200
	), 200