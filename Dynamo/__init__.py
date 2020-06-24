"""
Initialize DynamoDB Connection
"""

import boto3
from Dynamo.CreateTable import create_table
from flask import Response
from os import getenv
import simplejson as json

if getenv("LOCAL"):
    """ In case the app is being run locally for testing with an offline Dynamo Instance """
    ddb_resource = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')  # High Level Connection
    ddb_client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')  # Low Level Connection
else:
    """ In case Dynamo is being run in the cloud """
    ddb_resource = boto3.resource('dynamodb', region_name='us-east-1')  # High Level Connection
    ddb_client = boto3.client('dynamodb', region_name='us-east-1')  # Low Level Connection

table_name = 'UserProcesses'  # Name of table to operate on
table = ddb_resource.Table(table_name)  # Obtain Table instance from Dynamo
create_table(ddb_resource, ddb_client, table_name, 'user_id', 'S', 'tier_gsi', 'tier')  # Attempts to create table


def jsonify(obj):
    """ Jsonify with Decimal capabilities """
    json_st = json.dumps(obj)
    return Response(json_st, mimetype='application/json')
