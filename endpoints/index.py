""" Index """
from flask import Response
from endpoints import app_endpoints, decorate_if_not
import Dynamo
from Dynamo import jsonify
from flask_cognito import cognito_auth_required
from os import getenv
from Scraper.LawScraper import scrap_law
from flask import abort


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


@app_endpoints.route('/testp', methods=['GET'], strict_slashes=False)
@decorate_if_not(getenv('LOCAL'), cognito_auth_required)
def testp():
    """ Test Endpoint """
    process_id = '11001221500020160010300'
    scrapped = scrap_law(process_id)
    try:
        js = jsonify(scrapped)
        return js
    except TypeError:
        abort(400)
