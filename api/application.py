""" Flask Application """
from os import getenv

from flask import Flask, make_response, jsonify
from api.endpoints import application_endpoints

application = Flask(__name__)
application.register_blueprint(application_endpoints)


@application.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    application.run()
