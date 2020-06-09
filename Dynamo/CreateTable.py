""" Creates Table in Dynamo Db with Specific Hash and Range"""


def create_table(ddb_resource, ddb_client, table_name, hash_key, type_hash, idx_name_gsi, attr_gsi):
    """ Creates a Table in Dynamo if it does not exist already """

    existing_tables = ddb_client.list_tables()['TableNames']
    if table_name in existing_tables:
        return

    table_created = ddb_resource.create_table(
        TableName=table_name,

        KeySchema=[
            {
                'AttributeName': hash_key,
                'KeyType': 'HASH'
            }
        ],

        AttributeDefinitions=[
            {
                'AttributeName': hash_key,
                'AttributeType': type_hash
            },
            {
                'AttributeName': 'tier',
                'AttributeType': "S"
            }
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": idx_name_gsi,
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughput": {
                    "WriteCapacityUnits": 5,
                    "ReadCapacityUnits": 5
                },
                "KeySchema": [
                    {
                        "KeyType": "HASH",
                        "AttributeName": attr_gsi
                    }
                ],
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }

    )
    table_created.meta.client.get_waiter('table_exists').wait(TableName=table_name)
