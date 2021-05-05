$(function () {
    $("#checkInit").on('change', function () {
        if ($(this).is(':checked')) {
            $('#index_init').attr('value', 'true');
        } else {
            $('#index_init').attr('value', 'false');
        }

    //    $('#index_init').text($('#checkInit').val());
    });

});

$(function () {

    if ($('#checkInit').val() == "true") {
        console.log("istrue " + $('#checkInit').val()  );
        $('#checkInit').prop('checked', true);
    } else {
        $('#checkInit').prop('checked', false);
            console.log("isfalse  "+ $('#checkInit').val() );
    }

});



