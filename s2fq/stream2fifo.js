
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }


exports.handler = (event, context, callback) => {
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
    }

    callback(null, 'yeah ok');
}