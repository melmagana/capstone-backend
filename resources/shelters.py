import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

shelters = Blueprint('shelters', 'shelters')

@shelters.route('/', methods=['GET'])
def shelters_test():
	return 'shelters resource working'


### CREATE SHELTER ROUTE ###
@shelters.route('/', methods=['POST'])
def create_shelter():
	payload = request.get_json()
	print('- ' * 30)
	print('create_shelter payload')
	print(payload)

	add_shelter = models.Shelter.create(
		name=payload['name'],
		about=payload['about']
	)
	print('- ' * 30)
	print('add_shelter')
	print(add_shelter)
	print('- ' * 30)
	print('add_shelter.__dict__')

	shelter_dict = model_to_dict(add_shelter)

	# response
	return jsonify(
		data=shelter_dict,
		message=f"Successfully added {shelter_dict['name']}",
		status=201
	), 201