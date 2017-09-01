import boto3
import os
import datetime
import time
import json
from botocore.exceptions import ClientError



dest_table = os.environ['DEST_TABLE']
dest_region = os.environ['DEST_REGION']

sqs = boto3.client('sqs')
ddb = boto3.client('dynamodb',region_name=dest_region)

# We use wait time to try to end our function gracefully instead of being
# timed out by lambda
def wait_time_from_ttl(ttl):
    wt = int(.2 * ttl)
    if wt == 0:
        wt = 1
    return wt

def insert(body):
    newImage = body['newImage']
    print 'insert {}'.format(newImage)

    try:
        response = ddb.put_item(
            TableName=dest_table,
            Item=newImage,
            ConditionExpression='attribute_not_exists(id)'
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print 'unable to replicate insert: item with key {} exists in remote region'.format(body['keys'])
        else:
            raise
    else:
        print 'insert succeeded'

   

def modify(body):
    newImage = body['newImage']
    print 'modify using {}'.format(newImage)

    body_ts = newImage['ts']
    body_wid = newImage['wid']

    try:
        response = ddb.put_item(
            TableName=dest_table,
            Item=newImage,
            ConditionExpression='(:ts > ts) OR (:ts = ts AND :wid > wid)',
            ExpressionAttributeValues={
                ':ts': body_ts,
                ':wid': body_wid
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print 'unable to replicate modify with ts {} and wid {}'.format(body_ts, body_wid)
        else:
            raise
    else:
        print 'modify succeeded'

def remove(body):
    keys = body['keys']
    print 'remove {}'.format(keys)

    oldImage = body['oldImage']
    body_ts = oldImage['ts']

    response = ddb.delete_item(
        TableName=dest_table,
        Key=keys,
        ConditionExpression='attribute_not_exists(id) OR (:ts >= ts)',
        ExpressionAttributeValues={
            ':ts': body_ts
        }
    )

    print response

def process_body(msg):
    print 'handle {}'.format(msg)
    body = json.loads(msg)

    opcode = body['opcode']

    if opcode == 'INSERT':
        insert(body)
    elif opcode == 'MODIFY':
        modify(body)
    elif opcode == 'REMOVE':
        remove(body)
    else:
        print 'Unknown opcode: {}'.format(opcode)
    

def delete_message(queue_url,receipt_handle):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )   

def lambda_handler(event, context):
    queue_url = os.environ['QUEUE_URL']
    ttl = int(os.environ['TTL_SECONDS'])
    time_threshold_ms = 700 * ttl
    
    print 'runtime threshold: {}'.format(time_threshold_ms)
    
    start = time.mktime(datetime.datetime.now().timetuple()) * 1000
    wait_time = wait_time_from_ttl(ttl)

    print 'reading from {}'.format(queue_url)

    while True:
        now = time.mktime(datetime.datetime.now().timetuple()) * 1000
        remaining = now - start
        print 'cumulative: {}'.format(remaining)
        if remaining > time_threshold_ms:
            print 'function exiting to avoid lambda timeout'
            return
        
        print 'dequeue message'
        response = sqs.receive_message(
            QueueUrl = queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=5,
            WaitTimeSeconds=wait_time
        )

        if 'Messages' in response:
            receipt_handle = response['Messages'][0]['ReceiptHandle']
            body = response['Messages'][0]['Body'] 

            process_body(body)
            delete_message(queue_url, receipt_handle)

