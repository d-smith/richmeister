exports.handler = (event, context, callback) => {
    console.log('event');
    console.log(event);
    console.log('context');
    console.log(context);

    callback(null, 'yeah ok');
}