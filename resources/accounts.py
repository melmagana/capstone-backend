import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user

accounts = Blueprint('accounts', 'accounts')

@accounts.route('/')
def account_test():
	return 'accounts resource working'

### REGISTER ROUTE -- POST ###
@accounts.route('/register', methods=['POST'])
def register():
	payload= request.get_json()
	payload['name'] = payload['name']
	payload['email'] = payload['email'].lower()
	print(payload)

	# check if user exists
	try:
		models.Account.get(models.Account.email == payload['email'])

		# response
		return jsonify(
			data={},
			message=f"An account with the email {payload['email']} already exists",
			status=401
		), 401
	except models.DoesNotExist:

		# scramble password with bcrypt
		pw_hash = generate_password_hash(payload['password'])

		# create account
		create_account = models.Account.create(
			name=payload['name'],
			email=payload['email'],
			password=pw_hash
		)
		print('- ' * 30)
		print('\nthis is create_account:', create_account)

		# logs in account and starts session
		login_user(create_account)

		create_account_dict = model_to_dict(create_account)
		print('- ' * 30)
		print('\nthis is create_account_dict:', create_account_dict)

		# remove password
		create_account_dict.pop('password')

		return jsonify(
			data=create_account_dict,
			message=f"Successfully registered account for {create_account_dict['name']}",
			status=201
		), 201

### LOGIN ROUTE -- POST ###
@accounts.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	payload['name'] = payload['name']
	payload['email'] = payload['email']

	# look up account by email
	try:
		account = models.Account.get(models.Account.email == payload['email'])
		account_dict = model_to_dict(account)

		# account exists, check password
		# 1st Arg -- the encrypted password you are checking against
		# 2nd Arg -- the password attempt you are trying to verify
		password_is_good = check_password_hash(account_dict['password'], payload['password'])

		# check if password is valid
		if(password_is_good):
			login_user(account)

			# remove password
			account_dict.pop('password')

			# response
			return jsonify(
				data=account_dict,
				message=f"{account_dict['name']} successfully logged in!",
				status=200
			), 200

		# if password is invalid
		else: 
			print('password is bad')

			# response
			return jsonify(
				data={},
				message="Email or password is invalid",
				status=401
			), 401

	# if user does not exist
	except models.DoesNotExist:
		print('account does not exist')

		# response
		return jsonify(
			data={},
			message="Account does not exist",
			status=401
		), 401

### TEMPORARY ROUTE ###
@accounts.route('/logged_in_account', methods=['GET'])
def currently_logged():
	print('- ' * 30)
	print('current_user:', current_user)

	# current_user.is_authenticated allows you to see whether a user is logged in
	if not current_user.is_authenticated:

		# response
		return jsonify(
			data={},
			message="No users are currently logged in",
			status=401
		), 401

	# access to currently logged user
	else:
		account_dict = model_to_dict(current_user)
		account_dict.pop('password')

		# response
		return jsonify(
			data=account_dict,
			message=f"{account_dict['name']} is currently logged in",
			status=200
		), 200

### LOGOUT ROUTE -- GET ###
@accounts.route('/logout', methods=['GET'])
def logout():
	logout_user()

	# response
	return jsonify(
		data={},
		message="Successfully logged out!",
		status=200
	), 200
