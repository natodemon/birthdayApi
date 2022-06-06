import boto3

TABLE_NAME = 'user-records'
ddb = boto3.resource('dynamodb', endpoint_url='http://dynamodb-local:8000', region_name='eu-west-1')

table = ddb.create_table(
    TableName = TABLE_NAME,
    AttributeDefinitions = [
        {'AttributeName': 'username', 'AttributeType': 'S'}
    ],
    KeySchema = [
        {'AttributeName': 'username', 'KeyType': 'HASH'}
    ],
    ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
)
