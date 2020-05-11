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
	shelter=BooleanField()
	adopter=BooleanField()

	class Meta:
		database = DATABASE


class Shelter(Model):
	name=CharField()
	about=TextField()

	class Meta:
		database = DATABASE


class Dog(Model):
	name=CharField()
	breed=CharField()
	age=CharField()
	gender=CharField()
	personality_type=CharField()
	shelter=CharField()
	date_arrived=DateField(formats=['%Y-%m-%d'])
	status=CharField()

	class Meta:
		database = DATABASE

		
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Account, Dog, Shelter], safe=True)
	print('Connected to database and created tables if they were not already there.')

	DATABASE.close()
