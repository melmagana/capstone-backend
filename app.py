import os
from flask import Flask, g
from resources.users import users
from resources.dogs import dogs
import models
from flask_cors import CORS
from flask_login import LoginManager

DEBUG=True
PORT=8000

app = Flask(__name__)

### LoginManager Configuration ###
## SECRET/KEY FOR SESSIONS ##
app.secret_key = 'Milo is the best dog in the universe! This is not a secret.'
## INSTANTIATE LoginManager ##
login_manager = LoginManager()
## CONNECT APP WITH THE LOGIN MANAGER ##
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	try:
		print('loading the following user')
		user = models.User.get_by_id(user_id)
		return user

	except models.DoesNotExist:
		return None


@login_manager.unauthorized_handler
def unauthorized():

	# response
	return jsonify(
		data={
			'error': 'User not logged in'
		},
		message="You must have an account to access this resource",
		status=401
	), 401



### CORS -- CROSS ORIGIN RESOURCE SHARING ###
CORS(users, origins=['http://localhost:3000', 'https://perritos-camperos.herokuapp.com'], supports_credentials=True)
CORS(dogs, origins=['http://localhost:3000', 'https://perritos-camperos.herokuapp.com'], supports_credentials=True)




### "CONTROLLERS" ###
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(dogs, url_prefix='/api/v1/dogs')



### PSTGRESQL ###
@app.before_request
def before_request():
	"""Connect to the database before each request"""
	print('you should see this before each request')
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	"""Close the database connection after each request"""
	print('you should see this after each request')
	g.db.close()
	return response




@app.route('/')
def hello():
	return 'Hello, World!'


if 'ON_HEROKU' in os.environ:
	print('\non heroku!')
	models.initialize()

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)