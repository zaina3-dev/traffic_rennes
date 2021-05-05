// var intervalID = setInterval(update_values, 1000);

function update_values(url) {
    console.log("******** RUN ");
    $.getJSON($SCRIPT_ROOT + '/_stuff/' + url,

        function (data) {
            $('#result').text(data);
            console.log("query = " + data);
        });

};




function stopTextColor() {
clearInterval(intervalID);
}

