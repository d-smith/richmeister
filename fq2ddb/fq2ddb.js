
function sleep(time, callback) {
    var stop = new Date().getTime();
    while(new Date().getTime() < stop + time) {
        ;
    }
    callback();
}

exports.handler = (event, context, callback) => {
    var n = 0;
    for(;;) {
        sleep(1000, function(){
            console.log(`n is ${n}`);
            n = n + 1;
        });
    }
}