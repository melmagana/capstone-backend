import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

dogs = Blueprint('dogs', 'dogs')


### INDEX DOG ROUTE -- GET ###
@dogs.route('/', methods=['GET'])
def dogs_index():
	result = models.Dog.select()
	print('- ' * 20)
	print('result')
	print(result)

	dog_dicts = [model_to_dict(dog) for dog in result]
	print('_ ' * 20)
	print('dog_dicts')
	print(dog_dicts)

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
	print(payload)

	add_dog = models.Dog.create(
		name=payload['name'],
		breed=payload['breed'],
		age=payload['age'],
		gender=payload['gender'],
		personality_type=payload['personality_type'],
		shelter=payload['shelter'],
		date_arrived=payload['date_arrived'],
		status=payload['status']
	)

	print('- ' * 30)
	print('add_dog')
	print(add_dog)
	print('- ' * 30)
	print('add_dog.__dict__')
	print(add_dog.__dict__)

	dog_dict = model_to_dict(add_dog)

	# response
	return jsonify(
		data=dog_dict,
		message=f"Successfully addded {dog_dict['name']}",
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

