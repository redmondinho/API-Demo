from peewee import *
from playhouse.hybrid import hybrid_property

tasks_db = SqliteDatabase('data/tasks.db')


class Task(Model):
	user_id = IntegerField()

	class Meta:
		database = tasks_db


def init_db():
	tasks_db.connect()
	tasks_db.create_tables([Task])
