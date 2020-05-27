""" CRUD for DynamoDB Items"""
from botocore.exceptions import ClientError


def put_item(table, item):
    """ Puts an item into a dynamoDB table """
    try:
        response = table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(user_id)'
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    else:
        return response


def get_item(table, key, projection_expression=[], attr_names=[]):
    """ Gets an item from a dynamoDB table """

    parameters = {"Key": key}

    if projection_expression:
        parameters["ProjectionExpression"] = projection_expression

    if attr_names:
        parameters["ExpressionAttributeNames"] = attr_names

    try:
        response = table.get_item(**parameters)

    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    else:
        item = response.get('Item')
        return item


def update_item(table, key, up_expression, attr_values, attr_names={}):
    """ Updates an item from a dynamoDB table"""
    # UpdateExpression= "set info.rating = :r, info.plot=:p, info.actors=:a"

    try:
        parameters = {
            "Key": key,
            "UpdateExpression": up_expression,
            "ReturnValues": "UPDATED_NEW",
            "ConditionExpression": 'attribute_exists(user_id)'
        }

        if attr_names:
            parameters["ExpressionAttributeNames"] = attr_names
        if attr_values:
            parameters["ExpressionAttributeValues"] = attr_values

        response = table.update_item(**parameters)

    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    else:
        return response


def delete_item(table, key):
    """
    Deletes an item from a dynamoDB table

    By design DynamoDB doesn't throw error even if an item
    does not exist already
    """
    try:
        response = table.delete_item(
            Key=key
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    else:
        return response
