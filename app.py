from flask import Flask
from resources.accounts import accounts
from resources.shelters import shelters
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
def load_user(account_id):
	try:
		print('loading the following account')
		account = models.Account.get_by_id(account_id)
		return account

	except models.DoesNotExist:
		return None



### CORS -- CROSS ORIGIN RESOURCE SHARING ###
CORS(accounts, origins=['http://localhost:3000'], supports_credentials=True)
CORS(shelters, origins=['http://localhost:3000'], supports_credentials=True)



### "CONTROLLERS" ###
app.register_blueprint(accounts, url_prefix='/api/v1/accounts')
app.register_blueprint(shelters, url_prefix='/api/v1/shelters')



@app.route('/')
def hello():
	return 'Hello, World!'

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)