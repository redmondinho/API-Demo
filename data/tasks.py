from peewee import *
from playhouse.hybrid import hybrid_property

tasks_db = SqliteDatabase('data/tasks.db')

class BaseModelTasks(Model):
    class Meta:
            database = tasks_db


class Task(BaseModelTasks):
	user_id = IntegerField()
	title = CharField()
	description = CharField()



def init_db():
	tasks_db.connect()
	tasks_db.create_tables([Task])
	task_record = Task.create(user_id=1, title='My Test Tasks', description='This is the first task and it was created automatically')