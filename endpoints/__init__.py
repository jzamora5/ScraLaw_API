""" Blueprint for API and Aux Functions"""
from flask import Blueprint


def decorate_if_not(condition, decorator):
    """
    Returns an "Empty" decorator if a condition is met
    If not, it returns an actual functional decorator given
    """
    return decorator if not condition else lambda fn: fn


# Defines the blueprint configuration including a prefix for all endpoints
app_endpoints = Blueprint('app_endpoints', __name__, url_prefix='/api')

# Defines all of the endpoints that will make part of the blueprint
from endpoints.index import *
from endpoints.users import *
from endpoints.processes import *


