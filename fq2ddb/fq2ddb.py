import boto3
import os

sqs = boto3.client('sqs')

def process_body(body):
    print 'handle {}'.format(body)

def delete_message(queue_url,receipt_handle):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )   

def lambda_handler(event, context):
    queue_url = os.environ['QUEUE_URL']

    print 'reading from {}'.format(queue_url)

    while True:
        print 'dequeue message'
        response = sqs.receive_message(
            QueueUrl = queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=5,
            WaitTimeSeconds=5
        )

        if 'Messages' in response:
            receipt_handle = response['Messages'][0]['ReceiptHandle']
            body = response['Messages'][0]['Body'] 

            process_body(body)
            delete_message(queue_url, receipt_handle)

