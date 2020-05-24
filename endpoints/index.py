""" Index """
from flask import Response
from endpoints import app_endpoints, decorate_if_not
import Dynamo
from Dynamo import jsonify
from flask_cognito import cognito_auth_required
from os import getenv


@app_endpoints.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_endpoints.route('/test', methods=['GET'], strict_slashes=False)
@decorate_if_not(getenv('LOCAL'), cognito_auth_required)
def test():
    """ Test Endpoint """
    response = Dynamo.table.scan()
    items = response['Items']
    return jsonify(items)
