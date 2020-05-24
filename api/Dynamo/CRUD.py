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


def get_item(table, key):
    """ Gets an item from a dynamoDB table """
    try:
        response = table.get_item(
            Key=key
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    else:
        item = response.get('Item')
        return item


def update_item(table, key, up_expression, attr_values):
    """ Updates an item from a dynamoDB table"""
    # UpdateExpression= "set info.rating = :r, info.plot=:p, info.actors=:a"
    try:
        response = table.update_item(
            Key=key,
            UpdateExpression="SET" + up_expression,
            ExpressionAttributeValues=attr_values,
            ReturnValues="UPDATED_NEW",
            ConditionExpression='attribute_exists(user_id)'
        )
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
