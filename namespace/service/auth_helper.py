from flask import request
from functools import wraps 
from flask_restplus import abort
from uuid import uuid4
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256

from data.users import Token, User
#from config import requests_per_token

# Validate supplied token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if 'X-API-KEY' in request.headers:

            try:
                supplied_token = request.headers['X-API-KEY']
            except:
                abort(401)

            # Get token record
            try:
                token_record = Token.get(Token.token == supplied_token)
            except:
                abort(401)

            # Increase request counter
            token_record.requests += 1

            # Check max requests
            if token_record.requests > 100:
                token_record.expiry = datetime.utcnow()
                token_record.save()
                return abort(429, 'You have exceeded the request limit, the current token has now expired.')

            token_record.save()

            # Check expiry date
            if token_record.expiry  < datetime.utcnow():
                return abort(401, 'Error Supplied token expired {0} UTC.'.format(token_record.expiry))

        else:
            abort(401)

        # Make the current user available
        kwargs['user'] = User.get(User.id==token_record.user_id)

        return f(*args, **kwargs)

    return decorated


# Manage user and token creation
def manage_user_token(email, password):

        # Check for existing user
        try:
            user_record = User.get(User.email==email)

            # Check password
            hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
            if not(pbkdf2_sha256.verify(password, hash)):
                abort(401)

        except:
            abort(401)

        # Check for valid token
        try:
            token_record = Token.get(Token.user_id==user_record.id, Token.expiry>=datetime.utcnow(), Token.requests<requests_per_token)
        except:

            # Create new token
            token = str(uuid4())
            date_created = datetime.utcnow()
            expiry_date = date_created + timedelta(hours=1)

            try:
                token_record = Token.create(token=token, created=date_created, expiry=expiry_date, user_id=user_record.id)
                token_record.save()
            except:
                return False, {}


        return True, token_record