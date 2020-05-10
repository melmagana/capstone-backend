import models
from flask import Blueprint

dogs = Blueprint('dogs', 'dogs')

@dogs.route('/', methods=['GET'])
def dogs_test():

	return 'dogs resource working'