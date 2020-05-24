""" Blueprint for API """
from flask import Blueprint


application_endpoints = Blueprint('application_endpoints', __name__, url_prefix='/api')

from api.endpoints.index import *
from api.endpoints.users import *
