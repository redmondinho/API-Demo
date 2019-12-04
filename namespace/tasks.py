from flask_restplus import Resource, Namespace, fields, reqparse
from flask import request
from datetime import datetime

from namespace.service.auth_helper import token_required
from data.tasks import Task

api = Namespace('task', description='Manage user task events.')

task_response = api.model('task_data', {
    'id' : fields.Integer,
    })

full_task_response = api.model('task_data', {
    'id' : fields.Integer,
    'title' : fields.String,
    'description' : fields.String
    })

task_list_response = api.model('tasks_list_data', {
	'tasks' : fields.List(fields.Nested(full_task_response))
    })

task_model = api.model('new-task', {
    'title' : fields.String(required=True, description='Task title.'),
    'description' : fields.String(description='Task description.')
    })



task_parser = reqparse.RequestParser()
task_parser.add_argument('title', required=True, help='Enter a title for your task.')
task_parser.add_argument('description', help='Enter an optional description for your task.')


@api.route('/')
class Tasks_Route(Resource):

	@token_required
	@api.doc(description='Return all user tasks.', security='apikey')
	@api.marshal_with(task_list_response)
	def get(self,user):
		try:
			tasks = Task.select().where(Task.user_id==1)
		except:
			pass

		return {'tasks' : tasks}


	@token_required
	@api.doc(description='Create a new Task for the current user.', security='apikey')
	@api.marshal_with(task_response)
	@api.expect(task_model, validate=True)
	def post(self, user):

		# Get supplied arguments
		args = task_parser.parse_args()
		title = args['title']
		description = args['description']

		# Create task
		try:
			new_task = Task.create(user_id=user.id,title=title,description=description)
			return new_task
		except:
			app.logger.error('Error creating new task')
			api.abort(500)


@api.route('/<int:task_id>')
class Task_Route(Resource):

	@token_required
	@api.doc(description='Return supplied user task detail.', security='apikey', params={'task_id' : 'A Task Id'})
	@api.marshal_with(full_task_response)
	def get(self, task_id, user):
		try:
			task = Task.get(Task.id==task_id)
		except:
			return api.abort(404)
		return task