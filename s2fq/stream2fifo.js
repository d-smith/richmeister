
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

var AWS = require('aws-sdk');
var sqs = new AWS.SQS();


exports.handler = (event, context, callback) => {
    const queueUrl = process.env.QUEUE_URL;
    const queueName = process.env.QUEUE_NAME;

    console.log('event');
    console.log(event);
    console.log('context');
    console.log(context);

    for (let record of event.Records) {
        //console.log(record.dynamodb)
        //console.log(record.dynamodb.Keys);
        //console.log(record.dynamodb.NewImage);
        

        //Is replication indicated? Note we can only check on
        //inserts and updates as there is no way to inject replication
        //context on delete
        if(record.eventName != 'REMOVE' && record.dynamodb.NewImage.replicate == undefined) {
            console.log('Replication not indicated',record.dynamodb.Keys)
            continue;
        }
        
        //Replication indicated - are the timestamp and write id fields
        //available?
        let image = record.dynamodb.NewImage;
        if (record.eventName == 'REMOVE') {
            image = record.dynamodb.OldImage
        }
        
        if (image.ts == undefined || image.wid == undefined) {
            console.log('Replication requested but ts and/or wid fields not present', image);
            continue;
        }
        
        console.log('Replicating item with key', record.dynamodb.Keys)
        
        const ddbCtx = {};
        ddbCtx.timestamp = Date.now();
        ddbCtx.opcode = record.eventName;
        ddbCtx.keys = record.dynamodb.Keys;
        ddbCtx.newImage = record.dynamodb.NewImage;
        ddbCtx.oldImage = record.dynamodb.OldImage;
        ddbCtx.writeId = uuidv4();
        
        //Important: we need to remove the replicate property, otherwise when
        //we update remote copies, they would replicate it back to use. The
        //cycle would be broken by the merge conflict detection, but we want
        //to eliminate the extra processing and cost up front when possible.
        if (ddbCtx.newImage !== undefined) {
            delete ddbCtx.newImage.replicate
        }

        console.log(ddbCtx)

        const params = {
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