import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

shelters = Blueprint('shelters', 'shelters')

@shelters.route('/', methods=['GET'])
def shelters_test():
	return 'shelters resource working'

@shelters.route('/', methods=['POST'])
def create_shelter():
	payload = request.get_json()
	print('- ' * 30)
	print('\nshelters payload:', payload)

	add_shelter = models.Shelter.create(
		name=payload['name'],
		city=payload['city'],
		state=payload['state'],
		address=payload['address'],
		country=payload['country'],
		about=payload['about']
	)
	print('\n- ' * 30)
	print('this is shelter #', add_shelter)
	print('\n- ' * 30)
	print('this is add_shelter.__dict__:', add_shelter.__dict__)

	shelter_dict = model_to_dict(add_shelter)

	# response
	return jsonify(
		data=shelter_dict,
		message=f"Successfully added the shelter {shelter_dict['name']}",
		status=201
	), 201