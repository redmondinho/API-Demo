from peewee import *
from playhouse.hybrid import hybrid_property
from config import requests_per_token


users_db = SqliteDatabase('data/users.db')


class User(Model):
	name = CharField()
	created = DateTimeField()
	email = CharField(unique=True)
	active = IntegerField(default=1)
	password = CharField(null=True)

	class Meta:
		database = users_db


class Token(Model):
	token = CharField(unique=True)
	created = DateTimeField()
	expiry = DateTimeField()
	requests = IntegerField(default=0)
	user_id = ForeignKeyField(User, backref='User', null=True)
	max_requests = IntegerField(default=requests_per_token)

	@hybrid_property
	def requests_remaining(self):
		return self.max_requests - self.requests

	class Meta:
		database = users_db


def init_db():
	users_db.connect()
	users_db.create_tables([Token, User])

	# Create base user
	from datetime import datetime
	from passlib.hash import pbkdf2_sha256
 
	hash = pbkdf2_sha256.encrypt("manager", rounds=200000, salt_size=16)
	base_user = user_record = User.create(name='Tom', email='redmondinho@gmail.com', created=datetime.utcnow(), password=hash)
