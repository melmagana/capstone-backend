import models
from flask import Blueprint

shelters = Blueprint('shelters', 'shelters')

@shelters.route('/', methods=['GET'])
def shelters_test():
	return 'shelters resource working'