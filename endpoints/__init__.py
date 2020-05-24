""" Blueprint for API """
from flask import Blueprint


app_endpoints = Blueprint('app_endpoints', __name__, url_prefix='/api')

from endpoints.index import *
from endpoints.users import *
