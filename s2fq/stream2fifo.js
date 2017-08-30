exports.handler = (event, context, callback) => {
    console.log('event');
    console.log(event);
    console.log('context');
    console.log(context);

    for (let record of event.Records) {
        console.log(record.dynamodb.Keys);
        console.log(record.dynamodb.NewImage);
    }

    callback(null, 'yeah ok');
}