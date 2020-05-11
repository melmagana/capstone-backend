import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user
import pprint

shelters = Blueprint('shelters', 'shelters')


### SHELTER INDEX ROUTE -- GET ###
@shelters.route('/', methods=['GET'])
def shelters_index():

	result = models.Shelter.select()
	print('- ' * 30)
	print('shelter result')
	print(result)

	shelter_dicts = [model_to_dict(shelter) for shelter in result]
	print('- ' * 30)
	print('shelter_dicts')
	print(shelter_dicts)

	for shelter_dict in shelter_dicts:
		# remove password
		shelter_dict['name'].pop('password')

	print('- ' * 30)
	print('shelter_dicts')
	print(shelter_dicts)

	# response
	return jsonify({
		'data': shelter_dicts,
		'message': f"Successfully found {len(shelter_dicts)} shelters",
		'status': 200
	}), 200


### CREATE SHELTER ROUTE ###
@shelters.route('/', methods=['POST'])
def create_shelter():
	payload = request.get_json()
	print('- ' * 30)
	print('create_shelter payload')
	print(payload)

	add_shelter = models.Shelter.create(
		name=current_user.id,
		about=payload['about']
	)
	print('- ' * 30)
	print('add_shelter')
	print(add_shelter)
	print('- ' * 30)
	print('add_shelter.__dict__')
	print(add_shelter.__dict__)

	shelter_dict = model_to_dict(add_shelter)
	shelter_dict['name'].pop('password')

	# response
	return jsonify(
		data=shelter_dict,
		message=f"Successfully added {shelter_dict['name']}",
		status=201
	), 201