""" Blueprint for API and Aux Functions"""
from flask import Blueprint


def decorate_if_not(condition, decorator):
    return decorator if not condition else lambda fn: fn


app_endpoints = Blueprint('app_endpoints', __name__, url_prefix='/api')

from endpoints.index import *
from endpoints.users import *
from endpoints.processes import *


