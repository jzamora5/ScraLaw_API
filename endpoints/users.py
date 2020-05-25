""" User Endpoints """

from datetime import datetime
import Dynamo
from Dynamo import jsonify
from Dynamo.CRUD import put_item, get_item, update_item, delete_item
from endpoints import app_endpoints, decorate_if_not
from flask import abort, make_response, request
from flask_cognito import cognito_auth_required
from os import getenv


allowed_keys = ['first_name', 'last_name', 'person_id_type', 'person_id', 'e_mail', 'tel']


@app_endpoints.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@decorate_if_not(getenv('LOCAL'), cognito_auth_required)
def get_user(user_id):
    """ Returns all the info from a user in DynamoDB"""

    key = {'user_id': user_id}
    response = get_item(Dynamo.table, key)
    if not response:
        abort(400, description="Failed Getting User")

    return jsonify(response)


@app_endpoints.route('/users/<user_id>', methods=['POST'], strict_slashes=False)
@decorate_if_not(getenv('LOCAL'), cognito_auth_required)
def create_user(user_id):
    """ Creates a new User in DynamoDB Table"""
    date_now = datetime.now()
    date_iso = date_now.isoformat()

    item = {
        'user_id': user_id,
        'first_name': "",
        'last_name': "",
        'person_id_type': "",
        'person_id': "",
        'e_mail': "",
        'tel': "",
        'created_at': date_iso,
        'updated_at': date_iso,
        'processes': []
    }
    response = put_item(Dynamo.table, item)

    if not response:
        abort(400, description="Failed Creating User")

    return make_response(jsonify(response), 201)


@app_endpoints.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@decorate_if_not(getenv('LOCAL'), cognito_auth_required)
def update_user(user_id):
    """ Updates a user's information """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    key = {'user_id': user_id}

    up_expression = []
    attr_values = {}

    for d_key, d_value in data.items():
        if d_key not in allowed_keys:
            continue
        up_expression.append(' {}={}'.format(d_key, ':' + d_key))
        attr_values[':' + d_key] = d_value

    up_expression = ", ".join(up_expression)

    response = ""

    if attr_values:
        up_expression += ', updated_at=:updated_at'
        date_iso = datetime.now().isoformat()
        attr_values[':updated_at'] = date_iso
        response = update_item(Dynamo.table, key, up_expression, attr_values)

    if not response:
        abort(400, description="Failed Updating User")

    return jsonify(response)


@app_endpoints.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@decorate_if_not(getenv('LOCAL'), cognito_auth_required)
def delete_user(user_id):
    """ Deletes a user from DynamoDB """
    key = {'user_id': user_id}

    response = delete_item(Dynamo.table, key)

    if not response:
        abort(400, description="Failed Deleting User")

    return make_response(jsonify({}), 200)
