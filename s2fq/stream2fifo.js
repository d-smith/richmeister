
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

var AWS = require('aws-sdk');
var sqs = new AWS.SQS();


exports.handler = (event, context, callback) => {
    let queueUrl = process.env.QUEUE_URL;
    let queueName = process.env.QUEUE_NAME;

    console.log('event');
    console.log(event);
    console.log('context');
    console.log(context);

    for (let record of event.Records) {
        console.log(record.dynamodb.Keys);
        console.log(record.dynamodb.NewImage);

        let ddbCtx = {};
        ddbCtx.timestamp = Date.now();
        ddbCtx.opcode = record.eventName;
        ddbCtx.keys = record.dynamodb.Keys;
        ddbCtx.newImage = record.dynamodb.NewImage;
        ddbCtx.writeId = uuidv4();

        console.log(ddbCtx)

        let params = {
            MessageBody: JSON.stringify(ddbCtx),
            QueueUrl: queueUrl,
            MessageDeduplicationId: uuidv4(),
            MessageGroupId: queueName
        };

        sqs.sendMessage(params, function(err,data) {
            if (err) console.log(err, err.stack); 
            else     console.log(data);
        });
    }

    callback(null, 'yeah ok');
}