from radish import given, when, then, step
import boto3

ddb_west = boto3.client('dynamodb', region_name='us-west-2')
ddb_east = boto3.client('dynamodb', region_name='us-east-1') 

@given("{thing:S} to delete")
def thing_to_delete(step, thing):
    step.context.thing = thing
    return

@when("I delete it")
def delete_it(step):
    response = ddb_east.delete_item(
        TableName='PKTestTable',
        Key={
            'Id':{'S':step.context.thing}
        }
    )

    print response


@then("result should be {this:S}")
def result_should_be(step, this):
    response = ddb_west.get_item(
        TableName='PKTestTable',
        Key={
            'Id':{'S':step.context.thing}
        }
    )

    print response

    if this == 'none':
        itemPresent = 'Item' in response
        assert itemPresent == False, "expected no item"
    else:
        item = response['Item']
        repl_region = item['region']['S']
        assert repl_region == this, "expected {} got {}".format(this, repl_region)