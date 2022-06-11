function idDupliCheck() {

    $('.nameInput').change(function () {
        $('#idCheckSuccess').hide();
        $('.idCheck').show();
        $('.nameInput').attr("checkResult", "fail");
    })

    if ($('.nameInput').val() == '') {
        alert('아이디를 입력해주세요!')
        return;
    }

    idCheck = document.querySelector('input[name="loginid"]');
    console.log(idCheck.value);

    $.ajax({
        url: '/id',
        type: 'POST',
        dataType: "JSON",
        data:{checkId: idCheck.value},
        success: function (response) {
            let msg = response;

            if (msg['message'] == 'id duplicated') {
                alert('이미 존재하는 아이디입니다.');
                idCheck.focus();
                return;
            } else if (msg['message'] == 'id ok') {
                alert('사용 가능한 아이디입니다.');
                $('.nameInput').attr("checkResult", "success");
                $('#idCheckSuccess').show();
                $('.idCheck').hide();
                return;
            }
        },
        error: function (response) {
            alert ('error');
        }
    });

}

$(document).ready( function() {
    $("#pw, #pwcon").keyup(function() {

        var pw1 = $('#pw').val();
        var pw2 = $('#pwcon').val();

        if (pw1 != "" && pw2 != "") {
            if (pw1 == pw2) {
                $('#pw').attr("checkPw", "success");
                $('#confirmMsg1').show();
                $('#confirmMsg2').hide();
                console.log($('#pw').attr("checkPw"));
            } else {
                $('#pw').attr("checkPw", "fail");
                $('#confirmMsg1').hide();
                $('#confirmMsg2').show();
                console.log($('#pw').attr("checkPw"));
            }
        }
    });
});

function checkAll() {
    if ($('.nameInput').attr("checkResult") == "fail") {
        alert('아이디 중복 체크를 해주세요!');
        return false;
    } else if ($('#pw').attr("checkPw") == "fail") {
        alert('비밀번호 양식을 확인해주세요!');
        return false;
    }
    return true;
}
