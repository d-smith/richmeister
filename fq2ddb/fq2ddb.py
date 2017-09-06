import boto3
import os
import datetime
import time
import json
from botocore.exceptions import ClientError


# Table config from environment
dest_table = os.environ['DEST_TABLE']
dest_region = os.environ['DEST_REGION']
stack_name = os.environ['STACK_NAME']

# Use metric namespace unique to the stack
metric_namespace = 'XtRepl' + stack_name

# SDK handles
sqs = boto3.client('sqs')
ddb = boto3.client('dynamodb',region_name=dest_region)
cw = boto3.client('cloudwatch')

def pub_statistic(name):
    response = cw.put_metric_data(
            Namespace=metric_namespace,
            MetricData=[
                {
                    'MetricName': name,
                    'Dimensions': [
                        {
                            'Name':'table',
                            'Value': dest_table
                        }
                    ],
                    'Timestamp' : datetime.datetime.utcnow(),
                    'Value':1.0,
                    'Unit': 'Count'
                }
            ]
        )
    print response


def hash_attribute(table_name):
    response = ddb.describe_table(
        TableName=table_name
    )
    
    table = response['Table']
    keySchema = table['KeySchema']
    
    for keyAttr in keySchema:
        if keyAttr['KeyType'] == 'HASH':
            return keyAttr['AttributeName']

def id_not_exists_condition(table_name):
    hash_attr = hash_attribute(table_name)
    return 'attribute_not_exists({})'.format(hash_attr)

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

    body_ts = newImage['ts']
    body_wid = newImage['wid']

    try:
        response = ddb.put_item(
            TableName=dest_table,
            Item=newImage,
            ConditionExpression='{} OR ((:ts > ts) OR (:ts = ts AND :wid > wid))'.format(id_not_exists_condition(dest_table)),
            ExpressionAttributeValues={
                ':ts': body_ts,
                ':wid': body_wid
            }
        )
    except ClientError as e:
        pub_statistic('ReplicatedInsertErrorCount')
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print 'unable to replicate insert: item with key {} exists in remote region'.format(body['keys'])
        else:
            raise
    else:
        print 'insert succeeded'
        pub_statistic('ReplicatedInsertCount')

   

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
        pub_statistic('ReplicatedModifyErrorCount')
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print 'unable to replicate modify with ts {} and wid {}'.format(body_ts, body_wid)
        else:
            raise
    else:
        print 'modify succeeded'
        pub_statistic('ReplicatedModifyCount')

def remove(body):
    keys = body['keys']
    print 'remove {}'.format(keys)

    oldImage = body['oldImage']
    body_ts = oldImage['ts']

    try:
        response = ddb.delete_item(
            TableName=dest_table,
            Key=keys,
            ConditionExpression='{} OR (:ts >= ts)'.format(id_not_exists_condition(dest_table)),
            ExpressionAttributeValues={
                ':ts': body_ts
            }
        )
    except ClientError as e:
        pub_statistic('ReplicatedRemoveErrorCount')
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print 'unable to replicate delete due to conditional check failed (key {})'.format(keys)
        else:
            raise
    else:
        print 'remove succeeded'
        pub_statistic('ReplicatedRemoveCount')
   


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

def dump_config_context(queue_url, ttl):
    print 'config context:'
    print '\tqueue_url: {}'.format(queue_url)
    print '\tttl: {}'.format(ttl)
    print '\tdestination region'.format(dest_region)
    print '\tdestination table'.format(dest_table)

def lambda_handler(event, context):
    queue_url = os.environ['QUEUE_URL']
    ttl = int(os.environ['TTL_SECONDS'])
    time_threshold_ms = 700 * ttl

    dump_config_context(queue_url,ttl)
    
    print 'runtime threshold: {}'.format(time_threshold_ms)
    
    start = time.mktime(datetime.datetime.utcnow().timetuple()) * 1000
    wait_time = wait_time_from_ttl(ttl)

    while True:
        now = time.mktime(datetime.datetime.utcnow().timetuple()) * 1000
        remaining = now - start
        if remaining > time_threshold_ms:
            print 'function exiting to avoid lambda timeout'
            return
        
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

