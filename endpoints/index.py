""" Index """
from flask import Response
from endpoints import app_endpoints
import Dynamo
from Dynamo import jsonify


@app_endpoints.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_endpoints.route('/test', methods=['GET'], strict_slashes=False)
def test():
    """ Test Endpoint """
    response = Dynamo.table.scan()
    items = response['Items']
    return jsonify(items)
