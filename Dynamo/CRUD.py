""" CRUD for DynamoDB Items"""
from botocore.exceptions import ClientError


def put_item(table, item):
    """ Puts an item into a dynamoDB table """
    try:
        # Tries to put item in table only if user id exists
        response = table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(user_id)'
        )

    except ClientError as e:
        # If there is an error give a response with the error message
        print(e.response['Error']['Message'])
        return False
    else:
        return response


def get_item(table, key, projection_expression=[], attr_names=[]):
    """ Gets an item from a dynamoDB table """

    parameters = {"Key": key}

    if projection_expression:
        # This expression identifies one or more attributes to
        # retrieve from the table
        parameters["ProjectionExpression"] = projection_expression

    if attr_names:
        # One or more substitution tokens for attribute names in
        # an expression
        parameters["ExpressionAttributeNames"] = attr_names

    try:
        response = table.get_item(**parameters)

    except ClientError as e:
        # If there is an error give a response with the error
        # message
        print(e.response['Error']['Message'])
        return False
    else:
        item = response.get('Item')
        return item


def update_item(table, key, up_expression, attr_values, attr_names={}):
    """ Updates an item from a dynamoDB table"""
    # UpdateExpression= "set info.rating = :r, info.plot=:p, info.actors=:a"

    try:
        # Includes some necessary parameters for updating items in a
        # Dynamo Table
        # UpdateExpression: An expression that defines one or more attributes
        # to be updated
        # Return Value: UPDATED NEW defines a response telling which attributes
        # where updated
        # Condition Expression defines an update only if a user id exists
        parameters = {
            "Key": key,
            "UpdateExpression": up_expression,
            "ReturnValues": "UPDATED_NEW",
            "ConditionExpression": 'attribute_exists(user_id)'
        }

        if attr_names:
            # One or more substitution tokens for attribute
            # names in an expression
            parameters["ExpressionAttributeNames"] = attr_names
        if attr_values:
            # One or more values that can be substituted in an expression
            parameters["ExpressionAttributeValues"] = attr_values

        response = table.update_item(**parameters)

    except ClientError as e:
        # If there is an error give a response with the error message
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
        # If there is an error give a response with the error message
        print(e.response['Error']['Message'])
        return False
    else:
        return response
