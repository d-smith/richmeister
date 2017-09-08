from radish import given, when, then, step
import os

import boto3

lambda_fn = os.environ['LAMBDA_FN']
lambda_east = boto3.client('lambda')
ddb_west = boto3.client('dynamodb', region_name='us-west-2')
ddb_east = boto3.client('dynamodb', region_name='us-east-1') 


@given("item {item:S}")
def modify_this_one(step, item):
    print 'modify_this_one'
    response = ddb_east.get_item(
        TableName='PKTestTable',
        Key={
            "Id": {
                "S": item
            }
        }
    )

    print response
    
    ddb_item = response['Item']

    step.context.ddb_item = ddb_item
    step.context.item = item

@when("I modify it")
def do_mod(step):
    
    for k in step.context.ddb_item:
        print '{} -> {}'.format(k,step.context.ddb_item[k])

    ddb_item = step.context.ddb_item
    ddb_item['replicate'] = {'BOOL': True}
    
    response = ddb_east.put_item(
        TableName='PKTestTable',
        Item=ddb_item
    )

    print response

@step("replication runs")
def replicate(step):
    print 'replication runs'
    response = lambda_east.invoke(
        FunctionName=lambda_fn,
        LogType='Tail'
    )

    print response

@then("I expect {region:S}")
def verify_mod_rep(step, region):
    print 'verify_mod_rep'

    response = ddb_west.get_item(
        TableName='PKTestTable',
        Key={
            "Id": {
                "S": step.context.item
            }
        }
    )
    print response

    repl_item = response['Item']

    repl_region = repl_item['region']['S']

    assert repl_region == region, "Remote region is {}, expected {}".format(repl_region, region)