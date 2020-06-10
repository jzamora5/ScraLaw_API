""" Flask Application """
import sys

sys.path.append('/var/app/current')

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from endpoints import app_endpoints
from flask_cognito import CognitoAuth

app = Flask(__name__)

app.config.update({
    'COGNITO_REGION': 'us-east-1',
    'COGNITO_USERPOOL_ID': 'us-east-1_sgeT5tm5u',

    # optional
    'COGNITO_APP_CLIENT_ID': '3rj5a30prom7dudokc1b5dog4l',  # client ID you wish to verify user is authenticated against
    'COGNITO_CHECK_TOKEN_EXPIRATION': True,  # disable token expiration checking for testing purposes
    'COGNITO_JWT_HEADER_NAME': 'X-MyApp-Authorization',
    'COGNITO_JWT_HEADER_PREFIX': 'Bearer'
})


app.register_blueprint(app_endpoints)

CognitoAuth(app)
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
    app.run()
