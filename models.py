from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('adoptions.sqlite')

class Account(UserMixin, Model):
	name=CharField()
	city=CharField()
	state=CharField()
	country=CharField()
	email=CharField(unique=True)
	password=CharField()


	class Meta:
		database = DATABASE
		
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Account], safe=True)
	print('Connected to database and created tables if they were not already there.')

	DATABASE.close()
