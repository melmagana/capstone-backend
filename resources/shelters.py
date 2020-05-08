import models
from flask import Blueprint, request

shelters = Blueprint('shelters', 'shelters')

@shelters.route('/', methods=['GET'])
def shelters_test():
	return 'shelters resource working'

@shelters.route('/', methods=['POST'])
def create_shelter():
	payload = request.get_json()
	print('- ' * 30)
	print('shelters payload:', payload)

	add_shelter = models.Shelter.create(
		name=payload['name'],
		city=payload['city'],
		state=payload['state'],
		address=payload['address'],
		country=payload['country'],
		about=payload['about']
	)
	print('- ' * 30)
	print('this is shelter #', add_shelter)

	return 'you hit the shelter create route - check terminal'