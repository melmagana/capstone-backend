from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('adoptions.sqlite')

class User(UserMixin, Model):
	name=CharField()
	city=CharField()
	state=CharField()
	country=CharField()
	email=CharField(unique=True)
	password=CharField()
	shelter=BooleanField()

	class Meta:
		database = DATABASE


class Dog(Model):
	name=CharField()
	breed=CharField()
	age=CharField()
	gender=CharField()
	personality_type=CharField()
	shelter=ForeignKeyField(User, backref='dogs')
	date_arrived=DateField(formats=['%Y-%m-%d'])
	status=CharField()

	class Meta:
		database = DATABASE

		
def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Dog], safe=True)
	print('Connected to database and created tables if they were not already there.')

	DATABASE.close()
