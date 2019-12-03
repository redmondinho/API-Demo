from flask_restplus import Resource, Namespace, fields
from namespace.service.auth_helper import token_required

api = Namespace('greeting', description='Get a greeting message from the server.')

message_response = api.model('message_data', {
    'greeting' : fields.String,
    'name' : fields.String
    })


@api.route('/')
class Message(Resource):

    @token_required
    @api.doc(description='It will respond with a greeting message to the name associated with the current token.', security='apikey')
    @api.marshal_with(message_response)
    def get(self, user):
        response_content = {'greeting' : 'Hello', 'name' : user.name}
        return response_content