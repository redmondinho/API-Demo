from flask_restplus import Resource, Namespace, fields, reqparse
from flask import request
from datetime import datetime

from namespace.service.auth_helper import token_required
from data.tasks import Task

api = Namespace('task', description='Manage user task events.')

task_response = api.model('task_data', {
    'task_id' : fields.Integer(attribute='id')
    })

task_list_response = api.model('tasks_list_data', {
    'tasks' : fields.List(fields.Nested(task_response))
    })



@api.route('/')
class Tasks(Resource):

	@token_required
	@api.doc(description='Return all user tasks.', security='apikey')
	@api.marshal_with(task_list_response)
	def get(self, user):
		tasks = Task.select().where(Task.user_id==user.id)
		return tasks


@api.route('/<int:task_id>')
class Task(Resource):

	@token_required
	@api.doc(description='Return supplied user task detail.', security='apikey', params={'task_id' : 'A Task Id'})
	@api.marshal_with(task_response)
	def get(self, task_id, user):
		return ''