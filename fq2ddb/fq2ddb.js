
var AWS = require('aws-sdk');
var sqs = new AWS.SQS();

exports.handler = (event, context, callback) => {
    let queueUrl = process.env.QUEUE_URL;
    console.log(`queue url: ${queueUrl}`)

    let params = {
        QueueUrl: queueUrl,
        MaxNumberOfMessages: 1,
        VisibilityTimeout: 5,
        WaitTimeSeconds: 10
    }
   
    console.log('receive message');
    sqs.receiveMessage(params, function(err, data) {
        if (err) console.log(err, err.stack);
        else {
            console.log(data);
        }    
    });
    
}