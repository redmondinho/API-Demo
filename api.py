from flask import Flask, redirect
from flask_restplus import Api
import logging
from logging import Formatter, FileHandler

app = Flask(__name__)

# Set Authorisation
authorizations = {
    'apikey' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'X-API-KEY'
    }
}

# Create API instance
api = Api(app,
            version='0.1',
            title='My API',
            description='Placeholder for my API.',
            authorizations=authorizations)

app.config['RESTPLUS_MASK_SWAGGER'] = False

# Import namespaces
from namespace.message import api as message
from namespace.authentication import api as authentication
from namespace.tasks import api as tasks

# Add namespaces
api.add_namespace(authentication)
api.add_namespace(message)
api.add_namespace(tasks)


if __name__ == '__main__':
    file_handler = FileHandler('output.log')
    handler = logging.StreamHandler()
    file_handler.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(handler)
    app.logger.addHandler(file_handler)
    app.run(debug=True, host='0.0.0.0')