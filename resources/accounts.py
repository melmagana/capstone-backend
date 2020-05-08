import models
from flask import Blueprint

accounts = Blueprint('accounts', 'accounts')

@accounts.route('/')
def account_index():
	return 'accounts resource working'