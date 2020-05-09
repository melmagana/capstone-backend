import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

shelters = Blueprint('shelters', 'shelters')

@shelters.route('/', methods=['GET'])
def shelters_test():
	return 'shelters resource working'


### CREATE SHELTER ROUTE -- POST ###
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


### UPDATE SHELTER ROUTE -- PUT ###
@shelters.route('/<id>', methods=['PUT'])
def update_shelter(id):
	payload = request.get_json()

	update_query = models.Shelter.update(
		name=payload['name'],
		city=payload['city'],
		state=payload['state'],
		address=payload['address'],
		country=payload['country'],
		about=payload['about']
	).where(models.Shelter.id == id)

	num_of_rows_modified = update_query.execute()

	updated_shelter = models.Shelter.get_by_id(id)
	updated_shelter_dict = model_to_dict(updated_shelter)

	return jsonify(
		data=updated_shelter_dict,
		message=f"Successfully updated shelter with id: {id}",
		status=200
	), 200