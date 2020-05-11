import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user
import pprint

dogs = Blueprint('dogs', 'dogs')


### INDEX DOG ROUTE -- GET ###
@dogs.route('/', methods=['GET'])
def dogs_index():
	result = models.Dog.select()
	print('- ' * 30)
	print('result')
	print(result)

	dog_dicts = [model_to_dict(dog) for dog in result]
	print('_ ' * 30)
	print('dog_dicts')
	print(dog_dicts)

	for dog_dict in dog_dicts:
		# remove password
		dog_dict['shelter'].pop('password')

	# response
	return jsonify({
			'data': dog_dicts,
			'message': f"Successfully found {len(dog_dicts)} dog(s)",
			'status': 200
		}), 200


### CREATE DOG ROUTE -- POST ###
@dogs.route('/', methods=['POST'])
def create_dog():
	payload = request.get_json()
	print('- ' * 30)
	print('create_dog payload')
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(payload)

	add_dog = models.Dog.create(
		name=payload['name'],
		breed=payload['breed'],
		age=payload['age'],
		gender=payload['gender'],
		personality_type=payload['personality_type'],
		shelter=current_user.id,
		date_arrived=payload['date_arrived'],
		status=payload['status']
	)

	print('- ' * 30)
	print('add_dog')
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(add_dog)
	print('- ' * 30)
	print('add_dog.__dict__')
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(add_dog.__dict__)

	dog_dict = model_to_dict(add_dog)
	print('- ' * 30)
	print('dog_dict')
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(dog_dict['shelter']['name'])
	dog_dict['shelter']['name'].pop('password')
	# response
	return jsonify(
		data=dog_dict,
		message=f"Successfully added {dog_dict['name']}",
		status=201
	), 201


### DESTROY DOG ROUTE -- DELETE ###
@dogs.route('/<id>', methods=['DELETE'])
def delete_dog(id):
	delete_query = models.Dog.delete().where(models.Dog.id == id)
	num_of_rows_deleted = delete_query.execute()

	# response
	return jsonify(
		data={},
		message=f"Successfully deleted {num_of_rows_deleted} dog with id of {id}",
		status=200
	), 200


### UPDATE DOG ROUTE -- PUT ###
@dogs.route('/<id>', methods=['PUT'])
def update_dog(id):
	payload = request.get_json()
	update_query = models.Dog.update(
		name=payload['name'],
		breed=payload['breed'],
		age=payload['age'],
		gender=payload['gender'],
		personality_type=payload['personality_type'],
		shelter=payload['shelter'],
		date_arrived=payload['date_arrived'],
		status=payload['status']
	).where(models.Dog.id == id)

	num_of_rows_updated = update_query.execute()

	updated_dog = models.Dog.get_by_id(id)
	updated_dog_dict = model_to_dict(updated_dog)

	# response
	return jsonify(
		data=updated_dog_dict,
		message=f"Successfully updated a dog with the id of {id}",
		status=200
	), 200
