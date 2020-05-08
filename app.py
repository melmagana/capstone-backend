from flask import Flask
from resources.accounts import accounts
import models

DEBUG=True
PORT=8000

app = Flask(__name__)

### "CONTROLLERS" ###
app.register_blueprint(accounts, url_prefix='/api/v1/accounts')

@app.route('/')
def hello():
	return 'Hello, World!'

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)