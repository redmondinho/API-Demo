from flask_restplus import Resource, Namespace, fields, reqparse
from flask import request
from datetime import datetime

from namespace.service.auth_helper import token_required, manage_user_token
from data.users import Token, User

api = Namespace('authentication', description='Manage access to API.')

token_response = api.model('token_data', {
    'token' : fields.String,
    'expiry' : fields.DateTime(dt_format='iso8601'),
    'token-requests-remaining' : fields.Integer(attribute='requests_remaining')
    })


user_model = api.model('User', {
    'user-name' : fields.String(required=True, description='Your user name.'),
    'password' : fields.String(required=True, description='Your password.')
    })

user_parser = reqparse.RequestParser()
user_parser.add_argument('user-name', required=True, help='Enter your user name.')
user_parser.add_argument('password', required=True, help='Enter your password.')


@api.route('/')
class Authentication(Resource):

    @api.doc(description='Will return an access token for the supplied user account.')
    @api.marshal_with(token_response)
    @api.expect(user_model, validate=True)
    def post(self):

        # Get supplied arguments
        args = user_parser.parse_args()
        email = args['user-name']
        password = args['password']

        # Manage user token
        status, token_record = manage_user_token(email, password)

        if not status:
            app.logger.error('Error managing user token for {0}'.format(email))
            api.abort(500)

        return token_record

'''
@api.route('/check_expiry')
class Check_Expiry(Resource):


    @token_required
    @api.doc(description='Will return expiry date and requests level status for the supplied access token.', security='apikey')
    @api.marshal_with(token_response)
    def get(self, user_name):
        try: 
            token_record = Token.get(Token.token == request.headers['X-API-KEY'])
        except:
            api.abort(400)

        return token_record
'''
