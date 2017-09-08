from radish import given, when, then, step
import os
import boto3


lambda_fn = os.environ['LAMBDA_FN']
lambda_east = boto3.client('lambda')
ddb_west = boto3.client('dynamodb', region_name='us-west-2')
ddb_east = boto3.client('dynamodb', region_name='us-east-1')    

@given("an item with id {item_id:S}")
def have_id(step, item_id):
    step.context.id = item_id

@given("timestamp {ts:g}")
def have_ts(step, ts):
    step.context.ts = ts

@given("wid {wid:S}")
def have_wid(step, wid):
    step.context.wid = wid

@given("remote item {present:S}")
def remote_item_present(step, present):
    step.context.present = present

@given("remote ts {rts:g}")
def remote_ts(step, rts):
    step.context.rts = rts

@given("remote wid {rwid:S}")
def remote_wid(step, rwid):
    step.context.rwid = rwid
    setup_remote(step.context)

@when("I replicate the insert")
def do_when(step):
    insert_item_to_replicate(step.context)
    execute_lambda()

@then("I expect the remote ts {repts:d}")
def check_ts(step, repts):
    print 'check_ts'
    
    response = ddb_west.get_item(
        TableName='PKTestTable',
        Key={
            "Id": {
                "S": step.context.id
            }
        }
    )
    print response

    item = response['Item']
    remote_ts = int(item['ts']['N'])

    region = item['region']['S']
    step.context.region = region

    assert remote_ts == repts, "Remote ts is {}, expected {}".format(remote_ts, repts)

@then("I expect region to be {region:S}")
def check_region(step, region):
    retrieved_region = step.context.region
    assert retrieved_region == region, "Retrieved region is {}, expected {}".format(retrieved_region, region)

def setup_remote(ctx):
    if ctx.present == 'no':
        return

    response = ddb_west.put_item(
        TableName='PKTestTable',
        Item={
            "Id": {
                "S": ctx.id
            },
            "ts": {
                "N": str(ctx.rts)
            },
            "wid": {
                "S": ctx.rwid
            },
            "region": {
                "S":"west"
            }
        }
    )

    print response

def execute_lambda():
    response = lambda_east.invoke(
        FunctionName=lambda_fn,
        LogType='Tail'
    )

    print response

def insert_item_to_replicate(ctx):
    response = ddb_east.put_item(
        TableName='PKTestTable',
        Item={
            "Id": {
                "S": ctx.id
            },
            "ts": {
                "N": str(ctx.ts)
            },
            "wid": {
                "S": ctx.wid
            },
            "replicate": {
                "BOOL": True
            },
            "region": {
                "S":"east"
            }
        }
    )

    print response