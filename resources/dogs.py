import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

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


### DOG INDEX ROUTE (LOGGED IN USER) -- GET ###
@dogs.route('/our_dogs', methods=['GET'])
@login_required
def our_dogs_index():
	current_user_dog_dicts = [model_to_dict(dog) for dog in current_user.dogs]

	for dog_dict in current_user_dog_dicts:
		dog_dict['shelter'].pop('password')
	print('- ' * 30)
	print('current_user_dog_dicts')
	print(current_user_dog_dicts)

	# response
	return jsonify({
		'data': current_user_dog_dicts,
		'message': f"Successfully found {len(current_user_dog_dicts)} dog(s)",
		'status': 200
	}), 200


### CREATE DOG ROUTE -- POST ###
@dogs.route('/', methods=['POST'])
@login_required
def create_dog():

	# logic if user is not a shelter
	if current_user.shelter == False:

		#response
		return jsonify({
			'data': {},
			'message': "Not allowed, must be a shelter to add a dog",
			'status': 401
		}), 401

	# logic if user is a shelter
	else:
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
			shelter=current_user.id,
			date_arrived=payload['date_arrived'],
			status=payload['status'],
			image=payload['image']
		)

		print('- ' * 30)
		print('add_dog')
		print(add_dog)
		print('- ' * 30)
		print('add_dog.__dict__')
		print(add_dog.__dict__)

		dog_dict = model_to_dict(add_dog)
		print('- ' * 30)
		print('dog_dict')
		print(dog_dict['shelter'])
		dog_dict['shelter'].pop('password')

		# response
		return jsonify(
			data=dog_dict,
			message=f"Successfully added {dog_dict['name']}",
			status=201
		), 201


### DESTROY DOG ROUTE -- DELETE ###
@dogs.route('/<id>', methods=['DELETE'])
@login_required
def delete_dog(id):

	# logic if user is not a shelter
	if current_user.shelter == False:

		# response
		return jsonify(
			data={},
			message="Not allowed, must be shelter to delete a dog",
			status=401
		), 401

	# logic if user is a shelter
	else:
		try:
			# retrieve dog
			dog_to_delete = models.Dog.get_by_id(id)

			# logic to see if dog belongs to current user
			if dog_to_delete.shelter.id == current_user.id:
				dog_to_delete.delete_instance()

				# response
				return jsonify(
					data={},
					message=f"Successfully deleted dog with id of {id}",
					status=200
				),200

			# logic if dog does not belong to current user
			else:

				# response
				return jsonify(
					data={
						'error': '403 Forbidden'
					},
					message="Dog ID does not match user ID. Users can only delete their own dogs.",
					status=403
				), 403

			# logic if dog does not even exist
		except models.DoesNotExist:

			#response
			return jsonify(
				data={
					'error': '404 Not Found'
				},
				message="There is no dog with that ID",
				status=404
			), 404


### DOG UPDATE ROUTE -- PUT ###
@dogs.route('/<id>', methods=['PUT'])
@login_required
def update_dog(id):

	# logic if user is not a shelter
	if current_user.shelter == False:

		# response
		return jsonify(
			data={},
			message="Not allowed, must be shelter to update a dog",
			status=401
		), 401

	# logic if user is a shelter
	else:
		payload = request.get_json()
		dog_to_update = models.Dog.get_by_id(id)

		# logic to see if dog belongs to current user
		if dog_to_update.shelter.id == current_user.id:

			# then update
			if 'name' in payload:
				dog_to_update.name = payload['name']
			if 'breed' in payload:
				dog_to_update.breed = payload['breed']
			if 'age' in payload:
				dog_to_update.age = payload['age']
			if 'gender' in payload:
				dog_to_update.gender = payload['gender']
			if 'personality_type' in payload:
				dog_to_update.personality_type = payload['personality_type']
			if 'date_arrived' in payload:
				dog_to_update.date_arrived = payload['date_arrived']
			if 'status' in payload:
				dog_to_update.status = payload['status']
			if 'image' in payload:
				dog_to_update.image = payload['image']

			dog_to_update.save()

			updated_dog_dict = model_to_dict(dog_to_update)

			# remove password
			updated_dog_dict['shelter'].pop('password')

			# response
			return jsonify(
				data=updated_dog_dict,
				message=f"Successfully updated {updated_dog_dict['name']}",
				status=200
			), 200

		#logic if dog does not belong to current user
		else:

			# response
			return jsonify(
				data={
					'error': '403 Forbidden'
				},
				message="Dog ID does not match user ID. Users can only update their own dogs.",
				status=403

			), 403


### DOG SHOW ROUTE -- GET ###
@dogs.route('/<id>', methods=['GET'])
def show_dog(id):
	dog = models.Dog.get_by_id(id)

	dog_dict = model_to_dict(dog)
	dog_dict['shelter'].pop('password')

	return jsonify(
		data=dog_dict,
		message=f"Found dog with id of {id}",
		status=200
	), 200


### ADD INTEREST ###
@dogs.route('/interests/<id>', methods=['POST'])
@login_required
def add_interest(id):

	try:
		interest_to_add = (models.Interest.get((models.Interest.user_id == current_user.id) & (models.Interest.dog_id == id)))
		print(interest_to_add.user_id)
		print(model_to_dict(interest_to_add))
		print(current_user.id)

		# response
		return jsonify(
			data={},
			message="Dog already an interest",
			status=401
		), 401
	except models.DoesNotExist:
		models.Interest.create(
			user=current_user.id,
			dog=id
		)

		# response
		return jsonify(
			data={},
			message="Dog has now been added as an interest",
			status=200
		), 200


### DELETE INTEREST ###
@dogs.route('/interests/<id>', methods=['DELETE'])
def delete_interest(id):
	try:
		interest_to_delete = models.Interest.get((models.Interest.user_id == current_user.id) & (models.Interest.dog_id == id))
		interest_to_delete.delete_instance()

		# response
		return jsonify(
			data={},
			message="Deleted dog interest",
			status=200
		), 200
	except models.DoesNotExist:

		# response
		return jsonify(
			data={},
			message="Interest does not exist, therefore cannot delete",
			status=401
		), 401
