import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from playhouse.shortcuts import model_to_dict

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