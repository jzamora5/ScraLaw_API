""" Flask Application """
from flask_cognito import CognitoAuth
from endpoints import app_endpoints
from flask_cors import CORS
from flask import Flask, make_response, jsonify
import sys

# Adds the AWS Folder (ElasticBeanstalk) to the PythonPath
# so that modules are recognized
sys.path.append('/var/app/current')


app = Flask(__name__)

# Adds all AWS Cognito configurations into the flask config
app.config.update({
    'COGNITO_REGION': 'us-east-1',
    'COGNITO_USERPOOL_ID': 'us-east-1_sgeT5tm5u',

    # optional
    # client ID you wish to verify user is authenticated against
    'COGNITO_APP_CLIENT_ID': '3rj5a30prom7dudokc1b5dog4l',
    # disable token expiration checking for testing purposes
    'COGNITO_CHECK_TOKEN_EXPIRATION': True,
    'COGNITO_JWT_HEADER_NAME': 'X-MyApp-Authorization',
    'COGNITO_JWT_HEADER_PREFIX': 'Bearer'
})

# Registers the blueprint into the flask application
app.register_blueprint(app_endpoints)
# Registers the flask application into the authentication library
CognitoAuth(app)
# Establishes cors configuration for the flask application
CORS(app)


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    """ In case the Flask application is run as a main program """
    app.run()
