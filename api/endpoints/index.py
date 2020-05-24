""" Index """
from flask import Response
from api.endpoints import application_endpoints
import api.Dynamo as Dynamo
from api.Dynamo import jsonify


@application_endpoints.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@application_endpoints.route('/test', methods=['GET'], strict_slashes=False)
def test():
    """ Test Endpoint """
    response = Dynamo.table.scan()
    items = response['Items']
    return jsonify(items)
