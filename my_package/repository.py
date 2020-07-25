import os
from decimal import Decimal
import boto3


def _get_dynamo_table(table_name):
    dynamo_resource = boto3.resource('dynamodb', region_name=os.environ.get('DEPLOY_REGION'))
    table = dynamo_resource.Table(table_name)
    return table


def save_result(number, result):
    table_name = os.environ.get('DYNAMO_TABLE_NAME')
    table = _get_dynamo_table(table_name)
    item = {'key': str(number), 'value': Decimal(str(result))}
    table.put_item(Item=item)


def retrieve_result_for(number):
    table_name = os.environ.get('DYNAMO_TABLE_NAME')
    table = _get_dynamo_table(table_name)
    response = table.get_item(Key={'key': str(number)})
    item = response.get('Item')
    if item:
        return item['value']
