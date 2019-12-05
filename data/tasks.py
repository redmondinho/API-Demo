from peewee import *
from playhouse.hybrid import hybrid_property

tasks_db = SqliteDatabase('data/tasks.db')

class BaseModelTasks(Model):
    class Meta:
            database = tasks_db


class Task(BaseModelTasks):
	user_id = IntegerField()
	title = CharField()
	description = CharField(null=True)
	date_created = DateTimeField(null=True)
	date_modified = DateTimeField(null=True)


def init_db():
	tasks_db.connect()
	tasks_db.create_tables([Task])