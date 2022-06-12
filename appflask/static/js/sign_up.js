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

function confirmPw() {
    let pw = document.getElementById('pw');
    let pwcon= document.getElementById('pwcon');
    let cor = document.getElementById('confirmMsg1');
    let wro = document.getElementById('confirmMsg2');
    if (pw.value == "") {
        cor.style.display ="none";
        wro.style.display="none";
        pw.setAttribute('checkpw', 'fail');
    } else if (pw.value == pwcon.value) {
        cor.style.display ="block";
        wro.style.display="none";
        pw.setAttribute('checkpw', 'success');
    } else {
        cor.style.display ="none";
        wro.style.display="block";
        pw.setAttribute('checkpw', 'fail');
    }
}
