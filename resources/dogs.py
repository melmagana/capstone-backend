import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

dogs = Blueprint('dogs', 'dogs')

@dogs.route('/', methods=['GET'])
def dogs_test():

	return 'dogs resource working'

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

	return jsonify(
		data=dog_dict,
		message=f"Successfully addded {dog_dict['name']}",
		status=201
	), 201
