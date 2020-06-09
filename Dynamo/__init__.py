"""
Initialize DynamoDB Connection
"""

import boto3
from Dynamo.CreateTable import create_table
from flask import Response
from os import getenv
import simplejson as json

if getenv("LOCAL"):
    ddb_resource = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    ddb_client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
else:
    ddb_resource = boto3.resource('dynamodb', region_name='us-east-1')
    ddb_client = boto3.client('dynamodb', region_name='us-east-1')

table_name = 'UserProcesses'
table = ddb_resource.Table(table_name)
create_table(ddb_resource, ddb_client, table_name, 'user_id', 'S', 'tier_gsi', 'tier')


def jsonify(obj):
    """ Jsonify with Decimal capabilities """
    json_st = json.dumps(obj)
    return Response(json_st, mimetype='application/json')
