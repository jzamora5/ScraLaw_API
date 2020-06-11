""" Processes Endpoints"""

from datetime import datetime, timedelta
import Dynamo
from Dynamo import jsonify
from Dynamo.CRUD import put_item, get_item, update_item, delete_item
from endpoints import app_endpoints, decorate_if_not
from flask import abort, make_response, request
from flask_cognito import cognito_auth_required
from os import getenv
from Scraper.LawScraperBeautifulSoup import scrap_law


@app_endpoints.route('/processes/<process_id>/<user_id>', methods=['GET'], strict_slashes=False)
@decorate_if_not(getenv('LOCAL'), cognito_auth_required)
def get_process(process_id, user_id):
    """ Returns all the info from a user in DynamoDB"""

    key = {'user_id': user_id}
    projection_expression = "processes.#process_id"
    attr_names = {'#process_id': process_id}

    response = get_item(Dynamo.table, key,  projection_expression, attr_names)
    if not response:
        abort(400, description="Failed Getting Process")

    try:
        process = response.get("processes").get(process_id)
    except AttributeError:
        process = {}

    return jsonify(process)


@app_endpoints.route('/processes/user/<user_id>', methods=['GET'], strict_slashes=False)
@decorate_if_not(getenv('LOCAL'), cognito_auth_required)
def get_processes(user_id):
    """ Returns all the info from a user in DynamoDB"""

    key = {'user_id': user_id}
    projection_expression = "processes"

    response = get_item(Dynamo.table, key, projection_expression)
    if not response:
        abort(400, description="Failed Getting User")

    return jsonify(response)


@app_endpoints.route('/processes/<process_id>/<user_id>', methods=['POST', 'PUT'], strict_slashes=False)
@decorate_if_not(getenv('LOCAL'), cognito_auth_required)
def create_update_process(process_id, user_id):
    """ Creates or Updates a Process in a specific User in DynamoDB Table"""

    scrapped = scrap_law(process_id)
    # scrapped = {"Hello": "World", "Betty": "Holberton"}

    if not scrapped:
        abort(503, description="Scrapper Failed")

    key = {'user_id': user_id}

    # --------------- Code for created_at validation and tier ------------------------
    projection_expression = "processes.#process_id.#created_at, processes.#process_id.#tier"
    attr_names = {'#process_id': process_id, "#created_at": "created_at", "#tier": "tier"}

    date_iso = datetime.now().isoformat()
    try:
        process = get_item(Dynamo.table, key, projection_expression, attr_names)
        scrapped['created_at'] = process.get("processes").get(process_id).get('created_at')
        scrapped['tier'] = process.get("processes").get(process_id).get('tier')
    except:
        scrapped['created_at'] = date_iso
        scrapped['tier'] = "1"
    # ------------------------------------------------------------------------

    scrapped['updated_at'] = date_iso

    data = request.get_json()

    if data and isinstance(data, dict):
        tier = data.get("tier")
        if tier:
            scrapped['tier'] = tier

    up_expression = "SET processes.#process_id = :scr"
    attr_names = {'#process_id': process_id}
    attr_values = {':scr': scrapped}

    response = ""

    if attr_values:
        response = update_item(Dynamo.table, key, up_expression, attr_values, attr_names)

    if not response:
        abort(400, description="Failed Inserting/Updating process in User")

    return jsonify(response)


@app_endpoints.route('/processes/<process_id>/<user_id>', methods=['DELETE'], strict_slashes=False)
@decorate_if_not(getenv('LOCAL'), cognito_auth_required)
def delete_process(process_id, user_id):
    """ Deletes a process from a User in DynamoDB """

    key = {'user_id': user_id}
    date_iso = datetime.now().isoformat()

    # --------------- Code for tier validation ------------------------
    projection_expression = "processes.#process_id.#created_at, processes.#process_id.#updated_at"
    attr_names = {'#process_id': process_id, "#created_at": "created_at", "#updated_at": "updated_at"}

    try:
        process = get_item(Dynamo.table, key, projection_expression, attr_names)
        created_at = process.get("processes").get(process_id).get('created_at')
        updated_at = process.get("processes").get(process_id).get('updated_at')

    except:
        abort(400, description="Failed Getting process in User for Deletion")

    # -----------------------------------------------------------------

    created_obj = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S.%f').date()
    updated_obj = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S.%f').date()

    up_expression = 'REMOVE processes.#process_id'
    attr_names = {'#process_id': process_id}
    attr_values = {}

    response = update_item(Dynamo.table, key, up_expression, attr_values, attr_names)

    if not response:
        abort(400, description="Failed Deleting process in User")

    return jsonify(response)
