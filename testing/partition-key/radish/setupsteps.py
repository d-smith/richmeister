from radish import given, when, then, step
import boto3

ddb_west = boto3.client('dynamodb', region_name='us-west-2')
ddb_east = boto3.client('dynamodb', region_name='us-east-1')  

@given("east item {eid:S} {ets:d} {ewid:S}")
def east_create(step, eid, ets, ewid):
    response = ddb_east.put_item(
        TableName='PKTestTable',
        Item={
            "Id": {
                "S": eid
            },
            "ts": {
                "N": str(ets)
            },
            "wid": {
                "S": ewid
            },
            "region": {
                "S":"east"
            }
        }
    )

    print response

@given("west item {wid:S} {wts:d} {wwid:S}")
def west_create(step, wid, wts, wwid):
    response = ddb_west.put_item(
        TableName='PKTestTable',
        Item={
            "Id": {
                "S": wid
            },
            "ts": {
                "N": str(wts)
            },
            "wid": {
                "S": wwid
            },
            "region": {
                "S":"west"
            }
        }
    )

    print response

@then("I am ready to test")
def ready_to_test(step):
    return


