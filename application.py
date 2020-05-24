""" Flask Application """
import sys

sys.path.append('/var/app/current')

from flask import Flask, make_response, jsonify
from endpoints import app_endpoints


app = Flask(__name__)
app.register_blueprint(app_endpoints)


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
