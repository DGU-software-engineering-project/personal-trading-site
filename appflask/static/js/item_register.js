$(document).ready(function (e) {
                
    var fileTarget = $('#multiFiles');

    fileTarget.on('change', function() {
        var form_data = new FormData();
        var ins = document.getElementById('multiFiles').files.length;

        if (ins == 0) {
            $('#msg').html('<span style="color: red">Select at least one file</span');
                return;
        }

        form_data.append("file", document.getElementById('multiFiles').files[0]);

        for (var key of form_data.keys()) {
            console.log(key, ":", form_data.get(key));
        }

        $.ajax({
            url: '/file_upload', // 라우팅할 곳
            dataType: 'JSON',
            cache: false,
            contentType: false,
            processData: false,
            enctype: 'multipart/form-data',
            data: form_data,
            type: 'POST',
            success: function(response) {
                let msg = response;
                if (msg['filename']) {
                    $("#filename").val("/static/images/" + msg['filename']);
                    $("#photo").attr("src","/static/images/"+msg['filename']);
                    return;
                }
                alert("complete");
            },
            error: function (response) {
                alert("fail");
            }
        });

    })

});