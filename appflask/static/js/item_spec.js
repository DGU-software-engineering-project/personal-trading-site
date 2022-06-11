$(document).ready(function () {
    $('#followButtonClick').click(function() {

        console.log('{{iteminfo.ID}}');

        $.ajax({
            url: '/follow/{{iteminfo.ID}}',
            type: 'POST',

            success: function (response) {
                let msg = response;

                if (msg['message'] == 'sign in first') {
                    alert('Sign in first');
                    return;
                } else if (msg['message'] == 'Success Follow') {
                    alert('Success Follow');
                    return;
                }
            },
            error: function (response) {
                let msg = response;
                if (msg['message'] == 'do not follow yourself') {
                    alert('Do not follow yourself');
                    return;
                } else {
                    alert('Undefined error!');
                    return;
                }
            
            }
        });
    });
});